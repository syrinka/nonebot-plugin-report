<div align="center">

# nonebot-plugin-report

Push message from anywhere to your bot through webhook.

</div>

----

### 功能

该插件提供了一个位于 `/report` 的路由，通过此路由可向 bot 推送消息，实现消息推送机器人的功能

### 使用

webhook template
```json
{
    "token": "your token here",
    "title": "report title",
    "content": "report content",
    "send_to": "send to"
}
```

##### 字段

`token`: 令牌，当与设置的 `REPORT_TOKEN` 相同时才会推送消息，否则返回 403

`title`: 消息标题

`content`: 消息内容，* 必需字段

`send_to`: 推送对象。若为 `null` 则推送给所有超管；若为字符串则将其视为推送对象 user_id；若为字符串列表同上

##### 配置

`REPORT_TOKEN`: 令牌，若不设置则不会进行验证，即所有人都可以触发 webhook

`REPORT_ROUTE`: 路由，若与其它路由冲突可以更换该值，default: `/report`

`REPORT_TEMPLATE`: 消息模板，支持 `title` 与 `content` 两个字段，default: `{title}\n{content}`

### 其它

- 应向路由发送 POST 请求
- 仅支持发送纯文本消息

### 使用例

##### python

```bash
import requests
data = {'token': '...', 'content': '...'}
requests.post('http://127.0.0.1:8080/report', json=data)
```

##### curl

```bash
curl -L -X POST \
     -d '{"token": "...", "content": "..."}' \
     -H "Content-Type: application/json" \
     -- http://127.0.0.1:8080/report
```

### todo

- [x] 支持设置消息模板
- [ ] 支持使用 GET 触发
