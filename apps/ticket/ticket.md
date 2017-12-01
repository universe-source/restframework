---
title: 工单app的设计

time: 2017-12-01 16:26:57

---


## 1 Introduction
工单系统, ToC, 快速的解决用户提出的工单问题.


## 2 Requirement
### 2.1 User Requirement
- 创建工单, 设置期望解决时间
- 查看工单解决进度
- 确认工单解决
- 评价

### 2.2 Business Requirement
- 创建工单, 设置Urgency, 设置期望解决时间, 设置工单的分类以便下发到相应的部门, 创建人
- 工单的状态, 工单的承接人, 工单的解决历史记录
- 工单整体的消息回复
- 工单是否关闭
- 工单的评价度

### 2.3 Process
#### 2.3.1 Manager
1. 根据工单类型来决定后续的工单审核流程, 关联表:ticket_type
2. 工单状态表, 关联表: ticket_status

#### 2.3.2 User
1. 用户新建工单, 关联表:ticket_task
2. 用户对工单进行回复, 关联表: ticket_reply 

#### 2.3.3 Other
1. 工单操作, 记录不同状态的操作人, 关联表: ticket_operating

