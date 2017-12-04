---
title: 工单app的设计

time: 2017-12-01 16:26:57

---


## 1 Introduction
工单系统, ToC, 快速的解决用户提出的工单问题.


## 2 Logic
### 2.1 User Logic
- 创建工单, 设置期望解决时间
- 查看工单解决进度
- 查看工单并进行对话
- 确认工单解决
- 评价此次工单

### 2.2 Business Logic
- 创建工单, 设置Urgency, 设置期望解决时间, 设置工单的分类以便下发到相应的部门, 创建人
- 工单的状态, 工单的承接人, 工单的解决历史记录
- 查看工单所有对话并进行沟通
- 工单是否关闭
- 工单的评价度


## 3 Model
### 3.1 Manager
1. 根据工单类型来决定后续的工单审核流程, 关联表:ticket_type
2. 工单状态表, 关联表: ticket_status
3. 工单流程节点, 关联表: ticket_node

### 3.2 User
1. 用户新建工单, 关联表:ticket_task
2. 用户对工单进行回复, 关联表: ticket_reply 

### 3.3 Other
1. 工单操作, 记录不同状态的操作人, 关联表: ticket_operate


## 4 Specific Requirement
### 4.1 User
#### 4.1.1 Create a Ticket
创建工单, 用户填写工单标题, 工单类型, 工单描述, 并创建一个新的工单.
#### 4.1.2 Close a Ticket
用户手动关闭工单, 对于普通用户, 仅仅工单状态为:created时才能关闭工单, 其他状态不允许.
#### 4.1.3 Confirm a Ticket
用户确认工单已经成功处理完成, 仅仅工单状态为:handled时才能确认工单完成, 其他状态不允许.
#### 4.1.4 Score a Ticket
用户对确认后的工单进行评价, 仅仅工单状态为: confirmed
#### 4.1.5 Reply
用户插入一条新的留言, 或者回复某一条留言, 如果reply_to为空, 表示新插入留言.

### 4.2 Manager
> TODO: 在添加用户角色功能之后, 需要区分超级用户等各个不同角色之间的职能
#### 4.2.1 Add a New Ticket Type
添加一个新的工单类型, 其中涉及审核流程的创建. 目前默认所有受理人为管理员, 后期增加
角色功能之后, 会在审核流程添加"受理角色".

### 4.3 Acceptor
#### 4.3.1 Receive a Ticket
接受一个工单, 在接受工单之后, 其他接收人对该工单不可见.
更改工单状态: created->accepted, 如果工单已经处于accepted, 则不做更新操作.
#### 4.3.2 Handled a Ticket
确认某一个工单在该受理人这里已经处理完毕, 需要提前沟通用户. 之后处理人将工单从:
accepted->handled.
#### 4.3.3 Transfer a Ticket
将工单转移到下一个受理人, 并注明转移原因.
#### 4.3.4 Close a Ticket
沟通用户之后, 直接关闭订单.
#### 4.3.5 Reply
回复用户留言或者插入新的留言.
