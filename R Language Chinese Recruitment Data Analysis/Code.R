getwd()

library(dplyr)
library(stringr)
library(tidyr)
library(ggplot2)
data <- read.csv("招聘信息数据集2021-5.csv")
data <- data[sample(nrow(data), nrow(data) / 100), ]


unique(data$薪酬)
###数据预处理
##对薪酬列进行规范化处理
#1.提取并计算中间值
calculate_median_salary <- function(salary) {
  nums <- as.numeric(unlist(str_extract_all(salary, "\\d+\\.?\\d*")))
  if (length(nums) == 2) {
    return(mean(nums))
  } else {
    return(nums[1])
  }
}

#2.转换单位
convert_unit <- function(salary, multiplier) {
  if (str_detect(salary, "千")) {
    return(multiplier * 1000)
  } else if (str_detect(salary, "万")) {
    return(multiplier * 10000)
  } else {
    return(multiplier)
  }
}

#3.转换到年工资
convert_to_annual_salary <- function(salary) {
  multiplier <- calculate_median_salary(salary)
  multiplier <- convert_unit(salary, multiplier)
  
  if (str_detect(salary, "小时")) {
    return(multiplier * 8 * 28 * 12)
  } else if (str_detect(salary, "天")) {
    return(multiplier * 28 * 12)
  } else if (str_detect(salary, "月")) {
    return(multiplier * 12)
  } else {
    return(multiplier)
  }
}

#4.应用函数到数据集,赋值给薪酬_processed 以便对比是否更改成功
data$薪酬_processed <- sapply(data$薪酬, convert_to_annual_salary)

#1.删除薪酬列,并将薪酬_processed改名为薪酬
data <- subset(data, select = -薪酬)


data <- rename(data, 薪酬 = 薪酬_processed)



##对地点及需求列的信息进行提取

#1.提取地区信息

location <- function(x) {
  location <- str_extract(x, "^[^|]+")
  return(str_trim(location))
}

data <- data %>%
  mutate(地点 = sapply(地点及需求, location))


#2.提取经验信息
data$经验 <- sapply(data$地点及需求, function(x) {
  match <- regmatches(x, regexpr("\\d+-\\d+年经验|\\d+年经验|无需经验", x))
  if (length(match) == 0) return(NA)
  return(match)
})

#3.提取在校生/应届生信息
data$在校生或应届生 <- sapply(data$地点及需求, function(x) {
  match <- regmatches(x, regexpr("在校生/应届生", x))
  if (length(match) == 0) return(NA)
  return(match)
})

#4.提取学历信息

data <- data %>%
  mutate(学历 = str_extract(地点及需求, "博士|硕士|本科|大专|高中|中专|中技|初中"))
#5.提取招聘人数
data <- data %>%
  mutate(招聘人数 = str_extract(地点及需求, "招\\d+人")) %>%
  mutate(招聘人数 = str_extract(招聘人数, "\\d+")) 
#6.提取发布时间
  data <- data %>%
  mutate(发布时间 = str_extract(地点及需求, "\\d{2}-\\d{2}发布")) %>%
  mutate(发布时间 = str_replace(发布时间, "发布", ""))

#7.删除地点及需求列
data <- subset(data, select = -地点及需求)

##3.拆分地点列为城市和地区两列

split_location <- strsplit(data$地点, "-")

location_df <- do.call(rbind, split_location)

location_df <- data.frame(location_df)

names(location_df) <- c("城市", "地区")

data <- subset(data, select = -地点)

data <- cbind(data, location_df)

data$地区 <- ifelse(data$城市 == data$地区, NA, data$地区)



data_a=data



#1.市场概览


#1.1城市前六的饼状图
top_cities <- head(sort(table(data$城市), decreasing = TRUE), 6)
top_cities_df <- as.data.frame(top_cities)

ggplot(top_cities_df, aes(x = "", y = Freq, fill = Var1)) + 
  geom_bar(width = 1, stat = "identity") + 
  coord_polar("y", start=0) + 
  labs(title = "前六城市招聘分布", x = NULL, y = NULL, fill = "城市") +
  theme_minimal() + 
  theme(axis.text.x = element_blank())
#1.2行业前六饼状图
top_cities <- head(sort(table(data$行业), decreasing = TRUE), 6)
top_cities_df <- as.data.frame(top_cities)

ggplot(top_cities_df, aes(x = "", y = Freq, fill = Var1)) + 
  geom_bar(width = 1, stat = "identity") + 
  coord_polar("y", start=0) + 
  labs(title = "前六行业饼状图", x = NULL, y = NULL, fill = "行业") +
  theme_minimal() + 
  theme(axis.text.x = element_blank())
#1.3公司类型饼图
 #(不考虑重复)
company_type_df <- as.data.frame(table(data$公司类型))

ggplot(company_type_df, aes(x = "", y = Freq, fill = Var1)) + 
  geom_bar(width = 1, stat = "identity") + 
  coord_polar("y", start=0) + 
  labs(title = "公司类型分布(不考虑公司重复)", x = NULL, y = NULL, fill = "公司类型") +
  theme_minimal() + 
  theme(axis.text.x = element_blank())

 #(考虑重复)

unique_companies <- data %>%
  select(公司名, 公司类型) %>%
  distinct()

company_type_count <- unique_companies %>%
  group_by(公司类型) %>%
  tally()

ggplot(company_type_count, aes(x = "", y = n, fill = 公司类型)) +
  geom_bar(width = 1, stat = "identity") +
  coord_polar("y", start = 0) +  
  labs(title = "公司类型分布(考虑公司重复)", y = "公司数量", x = NULL) +
  theme_minimal() +
  theme(axis.text.x = element_blank(),
        axis.ticks = element_blank(),
        legend.position = "right")

#1.4公司规模饼状图
 #(不考虑重复)
company_size_df <- as.data.frame(table(data$规模))

ggplot(company_size_df, aes(x = "", y = Freq, fill = Var1)) + 
  geom_bar(width = 1, stat = "identity") + 
  coord_polar("y", start=0) + 
  labs(title = "公司规模分布(不考虑公司重复)", x = NULL, y = NULL, fill = "公司规模") +
  theme_minimal() + 
  theme(axis.text.x = element_blank())
 #(考虑重复)

unique_companies <- data %>%
  select(公司名, 规模) %>%
  distinct()

company_type_count <- unique_companies %>%
  group_by(规模) %>%
  tally()

ggplot(company_type_count, aes(x = "", y = n, fill = 规模)) +
  geom_bar(width = 1, stat = "identity") +
  coord_polar("y", start = 0) +  
  labs(title = "公司规模分布(考虑公司重复)", y = "公司数量", x = NULL) +
  theme_minimal() +
  theme(axis.text.x = element_blank(),
        axis.ticks = element_blank(),
        legend.position = "right")
#1.5各学历招聘人数之和
education_df <- as.data.frame(table(data$学历))

ggplot(education_df, aes(x = "", y = Freq, fill = Var1)) + 
  geom_bar(width = 1, stat = "identity") + 
  coord_polar("y", start=0) + 
  labs(title = "学历要求分布", x = NULL, y = NULL, fill = "学历要求") +
  theme_minimal() + 
  theme(axis.text.x = element_blank())

#1.6各个学历的招聘信息的数量

data_count <- data %>% 
  group_by(学历) %>%
  summarise(数据数量 = n())

ggplot(data_count, aes(x=学历, y=数据数量)) +
  geom_bar(stat="identity", fill="skyblue") +
  labs(title="各学历的数据数量", x="学历", y="数量") +
  theme_minimal()



#1.7各个学历的招聘人数之和(验证是否对于高学历需求较少)

data_sum <- data %>%
  group_by(学历) %>%
  summarise(招聘人数之和 = sum(招聘人数, na.rm = TRUE))
ggplot(data_sum, aes(x=学历, y=招聘人数之和)) +
  geom_bar(stat="identity", fill="coral") +
  labs(title="各学历的招聘人数之和", x="学历", y="招聘人数之和") +
  theme_minimal()



#2.1岗位需求与学历关系分析(以律师,软件工程师,教师,服务员这几个典型职业为例)



# 教师
teacher_jobs <- data[grep("教师", data$职位描述),]

education_counts <- table(teacher_jobs$学历)

pie(education_counts, main = "包含'教师'岗位的学历要求分布", col= c("#E57373", "#81C784", "#64B5F6", "#FFD54F", "#BA68C8")
, labels = names(education_counts))

# 服务员
teacher_jobs <- data[grep("服务员", data$职位描述),]

education_counts <- table(teacher_jobs$学历)

pie(education_counts, main = "包含'服务员'岗位的学历要求分布", col = c("#E57373", "#81C784", "#64B5F6", "#FFD54F", "#BA68C8"), labels = names(education_counts))

# 软件工程师
teacher_jobs <- data[grep("软件工程师", data$职位描述),]

education_counts <- table(teacher_jobs$学历)

pie(education_counts, main = "包含'软件工程师'岗位的学历要求分布", col =c("#E57373", "#81C784", "#64B5F6", "#FFD54F", "#BA68C8"), labels = names(education_counts))

# 律师
teacher_jobs <- data[grep("律师", data$职位描述),]

education_counts <- table(teacher_jobs$学历)

pie(education_counts, main = "包含'律师'岗位的学历要求分布", col = c("#E57373", "#81C784", "#64B5F6", "#FFD54F", "#BA68C8"), labels = names(education_counts))




#2.2不同城市的岗位需求分析(以律师,软件工程师,教师,服务员这几个典型职业为例)

# 教师
teacher_jobs <- data[grep("教师", data$职位描述),]
education_counts <- table(teacher_jobs$城市)

sorted_education_counts <- sort(education_counts, decreasing = TRUE)

top_six <- sorted_education_counts[1:6]

if (length(sorted_education_counts) > 6) {
  top_six["其他"] <- sum(sorted_education_counts[-(1:6)])
}

pie_labels <- paste(names(top_six), "\n", as.character(top_six))
pie(top_six, main = "发布包含'教师'岗位招聘信息的城市排名", col =c("#E57373", "#81C784", "#64B5F6", "#FFD54F", "#BA68C8"), labels = pie_labels)
# 服务员
teacher_jobs <- data[grep("服务员", data$职位描述),]
education_counts <- table(teacher_jobs$城市)

sorted_education_counts <- sort(education_counts, decreasing = TRUE)

top_six <- sorted_education_counts[1:6]

if (length(sorted_education_counts) > 6) {
  top_six["其他"] <- sum(sorted_education_counts[-(1:6)])
}

pie_labels <- paste(names(top_six), "\n", as.character(top_six))
pie(top_six, main = "发布包含'服务员'岗位招聘信息的城市排名", col = c("#E57373", "#81C784", "#64B5F6", "#FFD54F", "#BA68C8"), labels = pie_labels)

# 软件工程师
teacher_jobs <- data[grep("软件工程师", data$职位描述),]
education_counts <- table(teacher_jobs$城市)

sorted_education_counts <- sort(education_counts, decreasing = TRUE)

top_six <- sorted_education_counts[1:6]

if (length(sorted_education_counts) > 6) {
  top_six["其他"] <- sum(sorted_education_counts[-(1:6)])
}

pie_labels <- paste(names(top_six), "\n", as.character(top_six))
pie(top_six, main = "发布包含'软件工程师'岗位招聘信息的城市排名", col = c("#E57373", "#81C784", "#64B5F6", "#FFD54F", "#BA68C8"), labels = pie_labels)

# 律师
teacher_jobs <- data[grep("律师", data$职位描述),]
education_counts <- table(teacher_jobs$城市)

sorted_education_counts <- sort(education_counts, decreasing = TRUE)

top_six <- sorted_education_counts[1:6]

if (length(sorted_education_counts) > 6) {
  top_six["其他"] <- sum(sorted_education_counts[-(1:6)])
}

pie_labels <- paste(names(top_six), "\n", as.character(top_six))
pie(top_six, main = "发布包含'律师'岗位招聘信息的城市排名", col = c("#E57373", "#81C784", "#64B5F6", "#FFD54F", "#BA68C8"), labels = pie_labels)



#3.1.统计常见待遇
unique(data$待遇)

benefits_dict <- c("五险一金", "周末双休", "带薪年假", "绩效奖金", "节日福利", "专业培训", 
                   "年终奖金", "员工旅游", "餐饮补贴", "交通补贴", "全勤奖", "包住宿", "包吃", 
                   "高温补贴", "免费班车", "定期体检", "工龄奖金", "加班补贴", "弹性工作", 
                   "出国机会", "通讯补贴", "社保", "六险一金", "晋升机会", "下午茶", "团队奖励",
                   "扁平化管理","其他") 


benefits_count <- sapply(benefits_dict, function(benefit) {
  sum(grepl(benefit, data$待遇, fixed = TRUE))
})

benefits_df <- as.data.frame(benefits_count)
benefits_df <- benefits_df %>%
  rownames_to_column(var = "待遇") %>%
  arrange(desc(benefits_count))
ggplot(benefits_df, aes(x=reorder(待遇, benefits_count), y=benefits_count)) + 
  geom_bar(stat="identity", fill = "skyblue") +
  coord_flip() +   # 将图形横置，使待遇的标签更易读
  labs(title="各种待遇的计数", x="待遇", y="计数") +
  theme_minimal()



#3.2不同行业五险一金的比例(选取数量前六的行业)

data$是否五险一金 <- ifelse(grepl("五险一金", data$待遇), 1, 0)

target_industries <- c("互联网/电子商务", "房地产", "计算机软件", "电子技术/半导体/集成电路", "建筑/建材/工程", "教育/培训/院校")
filtered_data <- data[data$行业 %in% target_industries, ]

industry_insurance_ratio <- filtered_data %>%
  group_by(行业) %>%
  summarise(五险一金比例 = mean(是否五险一金, na.rm = TRUE))

ggplot(industry_insurance_ratio, aes(x = 行业, y = 五险一金比例)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  coord_flip() +
  labs(title = "各行业的五险一金比例", x = "行业", y = "五险一金比例") +
  theme_minimal()
#3.3不同行业绩效奖金的比例(选取数量前六的行业)
data$是否绩效奖金 <- ifelse(grepl("绩效奖金", data$待遇), 1, 0)

target_industries <- c("互联网/电子商务", "房地产", "计算机软件", "电子技术/半导体/集成电路", "建筑/建材/工程", "教育/培训/院校")
filtered_data <- data[data$行业 %in% target_industries, ]

industry_insurance_ratio <- filtered_data %>%
  group_by(行业) %>%
  summarise(绩效奖金比例 = mean(是否绩效奖金, na.rm = TRUE))

ggplot(industry_insurance_ratio, aes(x = 行业, y = 绩效奖金比例)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  coord_flip() +
  labs(title = "各行业的绩效奖金比例", x = "行业", y = "绩效奖金比例") +
  theme_minimal()
#3.4不同行业专业培训的比例(选取数量前六的行业)
data$是否专业培训 <- ifelse(grepl("专业培训", data$待遇), 1, 0)

target_industries <- c("互联网/电子商务", "房地产", "计算机软件", "电子技术/半导体/集成电路", "建筑/建材/工程", "教育/培训/院校")
filtered_data <- data[data$行业 %in% target_industries, ]

industry_insurance_ratio <- filtered_data %>%
  group_by(行业) %>%
  summarise(专业培训比例 = mean(是否专业培训, na.rm = TRUE))

ggplot(industry_insurance_ratio, aes(x = 行业, y = 专业培训比例)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  coord_flip() +
  labs(title = "各行业的专业培训比例", x = "行业", y = "专业培训比例") +
  theme_minimal()
#3.5不同行业年终奖金的比例(选取数量前六的行业)
data$是否年终奖金 <- ifelse(grepl("年终奖金", data$待遇), 1, 0)

target_industries <- c("互联网/电子商务", "房地产", "计算机软件", "电子技术/半导体/集成电路", "建筑/建材/工程", "教育/培训/院校")
filtered_data <- data[data$行业 %in% target_industries, ]

industry_insurance_ratio <- filtered_data %>%
  group_by(行业) %>%
  summarise(年终奖金比例 = mean(是否年终奖金, na.rm = TRUE))

ggplot(industry_insurance_ratio, aes(x = 行业, y = 年终奖金比例)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  coord_flip() +
  labs(title = "各行业的年终奖金比例", x = "行业", y = "年终奖金比例") +
  theme_minimal()
#3.6不同行业节日福利的比例(选取数量前六的行业)
data$是否节日福利 <- ifelse(grepl("节日福利", data$待遇), 1, 0)

target_industries <- c("互联网/电子商务", "房地产", "计算机软件", "电子技术/半导体/集成电路", "建筑/建材/工程", "教育/培训/院校")
filtered_data <- data[data$行业 %in% target_industries, ]

industry_insurance_ratio <- filtered_data %>%
  group_by(行业) %>%
  summarise(节日福利比例 = mean(是否节日福利, na.rm = TRUE))

ggplot(industry_insurance_ratio, aes(x = 行业, y = 节日福利比例)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  coord_flip() +
  labs(title = "各行业的节日福利比例", x = "行业", y = "节日福利比例") +
  theme_minimal()
#3.7不同行业带薪年假的比例(选取数量前六的行业)
data$是否带薪年假 <- ifelse(grepl("带薪年假", data$待遇), 1, 0)

target_industries <- c("互联网/电子商务", "房地产", "计算机软件", "电子技术/半导体/集成电路", "建筑/建材/工程", "教育/培训/院校")
filtered_data <- data[data$行业 %in% target_industries, ]

industry_insurance_ratio <- filtered_data %>%
  group_by(行业) %>%
  summarise(带薪年假比例 = mean(是否带薪年假, na.rm = TRUE))

ggplot(industry_insurance_ratio, aes(x = 行业, y = 带薪年假比例)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  coord_flip() +
  labs(title = "各行业的带薪年假比例", x = "行业", y = "带薪年假比例") +
  theme_minimal()


#3.8高薪酬是否意味着更好的待遇？用五险一金,专业培训,带薪年假为例


# 五险一金
data$Salary_Group <- cut(data$薪酬, breaks = c(-Inf, 50000,100000, 200000, Inf), labels = c("5万以下","5-10万", "10-20万", "20万以上"))

insurance_rate <- data %>%
  group_by(Salary_Group) %>%
  summarise(Insurance_Rate = mean(是否五险一金, na.rm = TRUE))

ggplot(insurance_rate, aes(x = Salary_Group, y = Insurance_Rate)) +
  geom_bar(stat = "identity", fill = "skyblue")+
  labs(title = "不同薪酬组的五险一金比例", x = "薪酬组", y = "五险一金比例")
#专业培训

data$Salary_Group <- cut(data$薪酬, breaks = c(-Inf, 50000,100000, 200000, Inf), labels = c("5万以下","5-10万", "10-20万", "20万以上"))

insurance_rate <- data %>%
  group_by(Salary_Group) %>%
  summarise(Insurance_Rate = mean(是否专业培训, na.rm = TRUE))

ggplot(insurance_rate, aes(x = Salary_Group, y = Insurance_Rate)) +
  geom_bar(stat = "identity", fill = "skyblue")+
  labs(title = "不同薪酬组的专业培训比例", x = "薪酬组", y = "专业培训比例")

#带薪年假

data$Salary_Group <- cut(data$薪酬, breaks = c(-Inf, 50000,100000, 200000, Inf), labels = c("5万以下","5-10万", "10-20万", "20万以上"))

insurance_rate <- data %>%
  group_by(Salary_Group) %>%
  summarise(Insurance_Rate = mean(是否带薪年假, na.rm = TRUE))

ggplot(insurance_rate, aes(x = Salary_Group, y = Insurance_Rate)) +
  geom_bar(stat = "identity", fill = "skyblue")+
  labs(title = "不同薪酬组的带薪年假比例", x = "薪酬组", y = "带薪年假比例")



#4.1经验对薪酬的影响


avg_salary_by_experience <- data %>%
  group_by(经验) %>%
  summarise(平均薪酬 = mean(薪酬, na.rm = TRUE)) %>%
  arrange(经验)  # 你可以根据实际情况决定是否排序

ggplot(avg_salary_by_experience, aes(x = 经验, y = 平均薪酬)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  labs(title = "不同经验的平均薪酬", x = "经验", y = "平均薪酬") +
  theme_minimal()
#5.定义招聘信息完整度,并新建一列保存信息招聘信息完整度


fields_2pts <- c("职位描述", "公司名", "公司类型", "规模", "薪酬", "行业", "待遇", "联系方式", "薪酬")
fields_1pt <- c("经验", "在校生或应届生", "城市", "地区","招聘人数","发布时间","学历")

data <- data %>%
  mutate(信息完整度 = rowSums(!is.na(.[fields_2pts]) * 2) + 
           rowSums(!is.na(.[fields_1pt])))




#5.1各招聘信息完整度的招聘信息数量



info_completeness_count <- table(data$信息完整度)

info_completeness_df <- data.frame(完整度 = names(info_completeness_count),
                                   数量 = as.numeric(info_completeness_count))

ggplot(info_completeness_df, aes(x = 完整度, y = 数量)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  theme_minimal() +
  labs(x = "招聘信息完整度", y = "招聘信息数量", title = "各招聘信息完整度的招聘信息数量柱状图") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


#5.2招聘信息完整度与薪酬关系

avg_sal <- data %>%
  group_by(信息完整度) %>%
  summarise(平均薪酬 = mean(薪酬, na.rm = TRUE))

ggplot(avg_sal, aes(x = as.factor(信息完整度), y = 平均薪酬)) +
  
  geom_bar(stat = "identity", fill = "skyblue") +
  
  labs(title = "招聘信息完整度与平均薪酬的关系",
       x = "招聘信息完整度",
       y = "平均薪酬") +
  theme_minimal()
#5.3探究招聘信息完整度与招聘人数的关系(看是不是因为要招聘的人数少所以信息填写不够用心导致不够完整)


data$招聘人数 <- as.numeric(data$招聘人数)

avg_hiring_count <- data %>%
  group_by(信息完整度) %>%
  summarise(平均招聘人数 = mean(招聘人数, na.rm = TRUE))

ggplot(avg_hiring_count, aes(x = 信息完整度, y = 平均招聘人数)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  theme_minimal() +
  labs(x = "信息完整度", y = "平均招聘人数", title = "招聘信息完整度与平均招聘人数的柱状图") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))



#6.1哪些城市为在校生和应届生提供更多的机会(选取前六城市)

target_cities <- c("深圳", "广州", "北京", "上海", "杭州", "武汉")

city_grad_counts <- data %>%
  filter(城市 %in% target_cities & 在校生或应届生 == "在校生/应届生") %>%
  group_by(城市) %>%
  summarise(数量 = n())

ggplot(city_grad_counts, aes(x = "", y = 数量, fill = 城市)) +
  geom_bar(width = 1, stat = "identity") +
  coord_polar("y", start = 0) +
  labs(title = "各城市招聘在校生/应届生数量", fill = "城市") +
  theme_minimal() +
  theme(axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x  = element_blank(),
        axis.ticks   = element_blank())
#6.2哪些行业为在校生和应届生提供更多的机会(选取前六行业)
target_cities <- c("互联网/电子商务", "房地产", "计算机软件", "电子技术/半导体/集成电路", "建筑/建材/工程", "教育/培训/院校")

city_grad_counts <- data %>%
  filter(行业 %in% target_cities & 在校生或应届生 == "在校生/应届生") %>%
  group_by(行业) %>%
  summarise(数量 = n())

ggplot(city_grad_counts, aes(x = "", y = 数量, fill = 行业)) +
  geom_bar(width = 1, stat = "identity") +
  coord_polar("y", start = 0) +
  labs(title = "各行业招聘在校生/应届生数量", fill = "行业") +
  theme_minimal() +
  theme(axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        axis.text.x  = element_blank(),
        axis.ticks   = element_blank())





#6.3总招聘人数前六的城市

top_cities_recruitment <- data %>%
  group_by(城市) %>%
  summarise(Total_Recruitment = sum(招聘人数, na.rm = TRUE)) %>%
  arrange(-Total_Recruitment) %>%
  head(6)

ggplot(top_cities_recruitment, aes(x = 城市, y = Total_Recruitment)) +
  geom_bar(stat = "identity",fill = "skyblue") +
  labs(title = "总招聘人数前六的城市", x = "城市", y = "招聘人数总和")
#6.4总招聘人数前六的城市的平均薪酬

selected_cities_salary <- data %>%
  filter(城市 %in% c("成都", "广州", "深圳", "武汉", "西安", "长沙")) %>%
  group_by(城市) %>%
  summarise(Avg_Salary = mean(薪酬, na.rm = TRUE))

ggplot(selected_cities_salary, aes(x = reorder(城市, Avg_Salary), y = Avg_Salary)) +
  geom_bar(stat = "identity",fill = "skyblue") +
  labs(title = "总招聘人数前六的城市的平均薪酬", x = "城市", y = "平均薪酬") +
  coord_flip()  


#6.5前六行业与在各城市的招聘总数的前六名
#互联网/电子商务
internet_recruitment <- data %>%
  filter(行业 == "互联网/电子商务") %>%
  count(城市) %>%
  arrange(-n) %>%
  head(6)

ggplot(internet_recruitment, aes(x = reorder(城市, n), y = n)) +
  geom_bar(stat = "identity",fill = "skyblue") +
  labs(title = "行业为互联网/电子商务在各城市的招聘总数前六名", x = "城市", y = "招聘数") +
  coord_flip() 


#房地产
internet_recruitment <- data %>%
  filter(行业 == "房地产") %>%
  count(城市) %>%
  arrange(-n) %>%
  head(6)

ggplot(internet_recruitment, aes(x = reorder(城市, n), y = n)) +
  geom_bar(stat = "identity",fill = "skyblue") +
  labs(title = "行业为房地产在各城市的招聘总数前六名", x = "城市", y = "招聘数") +
  coord_flip() 

#计算机软件
internet_recruitment <- data %>%
  filter(行业 == "计算机软件") %>%
  count(城市) %>%
  arrange(-n) %>%
  head(6)

ggplot(internet_recruitment, aes(x = reorder(城市, n), y = n)) +
  geom_bar(stat = "identity",fill = "skyblue") +
  labs(title = "行业为计算机软件在各城市的招聘总数前六名", x = "城市", y = "招聘数") +
  coord_flip() 

#电子技术/半导体/集成电路
internet_recruitment <- data %>%
  filter(行业 == "电子技术/半导体/集成电路") %>%
  count(城市) %>%
  arrange(-n) %>%
  head(6)

ggplot(internet_recruitment, aes(x = reorder(城市, n), y = n)) +
  geom_bar(stat = "identity",fill = "skyblue") +
  labs(title = "行业为电子技术/半导体/集成电路在各城市的招聘总数前六名", x = "城市", y = "招聘数") +
  coord_flip() 

#建筑/建材/工程
internet_recruitment <- data %>%
  filter(行业 == "建筑/建材/工程") %>%
  count(城市) %>%
  arrange(-n) %>%
  head(6)

ggplot(internet_recruitment, aes(x = reorder(城市, n), y = n)) +
  geom_bar(stat = "identity",fill = "skyblue") +
  labs(title = "行业为建筑/建材/工程在各城市的招聘总数前六名", x = "城市", y = "招聘数") +
  coord_flip() 

#教育/培训/院校
internet_recruitment <- data %>%
  filter(行业 == "教育/培训/院校") %>%
  count(城市) %>%
  arrange(-n) %>%
  head(6)

ggplot(internet_recruitment, aes(x = reorder(城市, n), y = n)) +
  geom_bar(stat = "identity",fill = "skyblue") +
  labs(title = "行业为教育/培训/院校在各城市的招聘总数前六名", x = "城市", y = "招聘数") +
  coord_flip() 



#7.公司规模的选择

#7.1公司规模与薪酬的关系
unique(data$规模)

scale_order <- c("少于50人", "50-150人", "150-500人", "500-1000人", "1000-5000人", "5000-10000人", "10000人以上")

avg_salary_by_scale <- data %>%
  group_by(规模) %>%
  summarise(平均薪酬 = mean(薪酬, na.rm = TRUE))

ggplot(avg_salary_by_scale, aes(x = factor(规模, levels = scale_order), y = 平均薪酬)) +
  geom_bar(stat="identity",fill = "skyblue") +
  coord_flip() +  # 水平柱状图
  labs(title = "公司规模与平均薪酬的关系", x = "公司规模", y = "平均薪酬") +
  theme_minimal()
#7.2公司规模与待遇的关系
unique(data$规模)
# 五险一金
insurance_rate <- data %>%
  group_by(规模) %>%
  summarise(Total = n(),
            With_Insurance = sum(是否五险一金 == 1)) %>%
  mutate(Insurance_Rate = With_Insurance / Total * 100)

ordered_sizes <- c("少于50人", "50-150人", "150-500人", "500-1000人", "1000-5000人", "5000-10000人", "10000人以上")

insurance_rate$规模 <- factor(insurance_rate$规模, levels = ordered_sizes)

ggplot(insurance_rate, aes(x = 规模, y = Insurance_Rate, fill = 规模)) +
  geom_bar(stat = "identity") +
  labs(title = "各规模公司的五险一金的比例", x = "规模", y = "五险一金比例 (%)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


# 带薪年假
insurance_rate <- data %>%
  group_by(规模) %>%
  summarise(Total = n(),
            With_Insurance = sum(是否带薪年假 == 1)) %>%
  mutate(Insurance_Rate = With_Insurance / Total * 100)
ordered_sizes <- c("少于50人", "50-150人", "150-500人", "500-1000人", "1000-5000人", "5000-10000人", "10000人以上")

insurance_rate$规模 <- factor(insurance_rate$规模, levels = ordered_sizes)

ggplot(insurance_rate, aes(x = 规模, y = Insurance_Rate, fill = 规模)) +
  geom_bar(stat = "identity") +
  labs(title = "各规模公司的带薪年假的比例", x = "规模", y = "带薪年假比例 (%)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# 专业培训
insurance_rate <- data %>%
  group_by(规模) %>%
  summarise(Total = n(),
            With_Insurance = sum(是否专业培训 == 1)) %>%
  mutate(Insurance_Rate = With_Insurance / Total * 100)
ordered_sizes <- c("少于50人", "50-150人", "150-500人", "500-1000人", "1000-5000人", "5000-10000人", "10000人以上")

insurance_rate$规模 <- factor(insurance_rate$规模, levels = ordered_sizes)

ggplot(insurance_rate, aes(x = 规模, y = Insurance_Rate, fill = 规模)) +
  geom_bar(stat = "identity") +
  labs(title = "各规模公司的专业培训的比例", x = "规模", y = "专业培训比例 (%)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


# 年终奖金
insurance_rate <- data %>%
  group_by(规模) %>%
  summarise(Total = n(),
            With_Insurance = sum(是否年终奖金 == 1)) %>%
  mutate(Insurance_Rate = With_Insurance / Total * 100)
ordered_sizes <- c("少于50人", "50-150人", "150-500人", "500-1000人", "1000-5000人", "5000-10000人", "10000人以上")

insurance_rate$规模 <- factor(insurance_rate$规模, levels = ordered_sizes)

ggplot(insurance_rate, aes(x = 规模, y = Insurance_Rate, fill = 规模)) +
  geom_bar(stat = "identity") +
  labs(title = "各规模公司的年终奖金的比例", x = "规模", y = "年终奖金比例 (%)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


# 绩效奖金
insurance_rate <- data %>%
  group_by(规模) %>%
  summarise(Total = n(),
            With_Insurance = sum(是否绩效奖金 == 1)) %>%
  mutate(Insurance_Rate = With_Insurance / Total * 100)
ordered_sizes <- c("少于50人", "50-150人", "150-500人", "500-1000人", "1000-5000人", "5000-10000人", "10000人以上")

insurance_rate$规模 <- factor(insurance_rate$规模, levels = ordered_sizes)

ggplot(insurance_rate, aes(x = 规模, y = Insurance_Rate, fill = 规模)) +
  geom_bar(stat = "identity") +
  labs(title = "各规模公司的绩效奖金的比例", x = "规模", y = "绩效奖金比例 (%)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))







#8.公司类型的选择
#8.1公司类型与薪酬的关系
average_salary_by_company_type <- data %>%
  group_by(公司类型) %>%
  summarise(平均薪酬 = mean(薪酬, na.rm = TRUE)) %>%
  arrange(-平均薪酬)  # 为了使柱状图更有序，这里按平均薪酬降序排列

ggplot(average_salary_by_company_type, aes(x = reorder(公司类型, 平均薪酬), y = 平均薪酬)) +
  geom_bar(stat = "identity",fill = "skyblue") +
  coord_flip() +  # 将柱状图变为水平的，使得公司类型标签更易读
  labs(title = "各类型公司的平均薪酬", x = "公司类型", y = "平均薪酬") +
  theme_minimal()


#8.2公司类型与薪酬的关系

# 五险一金
insurance_rate <- data %>%
  group_by(公司类型) %>%
  summarise(Total = n(),
            With_Insurance = sum(是否五险一金 == 1)) %>%
  mutate(Insurance_Rate = With_Insurance / Total * 100)


ggplot(insurance_rate, aes(x = 公司类型, y = Insurance_Rate, fill = 公司类型)) +
  geom_bar(stat = "identity") +
  labs(title = "各类型公司的五险一金的比例", x = "公司类型", y = "五险一金比例 (%)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# 带薪年假
insurance_rate <- data %>%
  group_by(公司类型) %>%
  summarise(Total = n(),
            With_Insurance = sum(是否带薪年假 == 1)) %>%
  mutate(Insurance_Rate = With_Insurance / Total * 100)


ggplot(insurance_rate, aes(x = 公司类型, y = Insurance_Rate, fill = 公司类型)) +
  geom_bar(stat = "identity") +
  labs(title = "各类型公司的带薪年假的比例", x = "公司类型", y = "带薪年假比例 (%)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# 专业培训
insurance_rate <- data %>%
  group_by(公司类型) %>%
  summarise(Total = n(),
            With_Insurance = sum(是否专业培训 == 1)) %>%
  mutate(Insurance_Rate = With_Insurance / Total * 100)


ggplot(insurance_rate, aes(x = 公司类型, y = Insurance_Rate, fill = 公司类型)) +
  geom_bar(stat = "identity") +
  labs(title = "各类型公司的专业培训的比例", x = "公司类型", y = "专业培训比例 (%)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# 年终奖金
insurance_rate <- data %>%
  group_by(公司类型) %>%
  summarise(Total = n(),
            With_Insurance = sum(是否年终奖金 == 1)) %>%
  mutate(Insurance_Rate = With_Insurance / Total * 100)


ggplot(insurance_rate, aes(x = 公司类型, y = Insurance_Rate, fill = 公司类型)) +
  geom_bar(stat = "identity") +
  labs(title = "各类型公司的年终奖金的比例", x = "公司类型", y = "年终奖金比例 (%)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


# 绩效奖励
insurance_rate <- data %>%
  group_by(公司类型) %>%
  summarise(Total = n(),
            With_Insurance = sum(是否绩效奖励 == 1)) %>%
  mutate(Insurance_Rate = With_Insurance / Total * 100)


ggplot(insurance_rate, aes(x = 公司类型, y = Insurance_Rate, fill = 公司类型)) +
  geom_bar(stat = "identity") +
  labs(title = "各类型公司的绩效奖励的比例", x = "公司类型", y = "绩效奖励比例 (%)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))










































