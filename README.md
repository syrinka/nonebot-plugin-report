<div align="center">

# nonebot-plugin-report

</div>

## 功能

该插件提供了一个位于 `/report` 的路由，通过此路由可直接向用户推送消息，实现消息推送机器人的功能

## 使用

请求体示例
```json
{
    "token": "your token here",
    "title": "report title",
    "content": "report content",
    "send_to": "send to"
}
```

### 字段

Field | Type | Desc
-- | -- | --
`token` | `Optional[str]` | 令牌；<br/>当与设置的 `REPORT_TOKEN` 相同时才会推送消息，否则返回 403
`title` | `Optional[str]` | 消息标题
`content` | `str` | 消息内容，*必需字段*
`send_from` | `Optional[ID]` | 推送消息的机器人 ID；<br/>若不设置，任意获取一个可用的机器人
`send_to` | `Optional[ID \| List[ID]]` | 推送用户 `user_id`；<br/>若为 `null` 则推送给所有超管；
`send_to_group` | `Optional[ID \| List[ID]]` | 推送群组 `group_id`

### 别名

部分字段提供有较短的别名：

Field | Alias
-- | --
`send_from` | `from`
`send_to` | `to`
`send_to_group` | `to_group`

别名的优先度低于原名，当且仅当原名未传入时，才会检查别名

### 配置

Field | Type | Desc | Default
-- | -- | -- | --
`REPORT_TOKEN` | `Optional[str]` | 令牌，若不设置则不会进行验证，所有人都可以触发 webhook |
`REPORT_FROM` | `Optional[ID]` | `send_from` 的默认值
`REPORT_ROUTE` | `str` | 路由，若与其它路由冲突可以更换该值，| `/report`
`REPORT_TEMPLATE` | `str` | 消息模板，支持 `title` 与 `content` 两个字段，| `{title}\n{content}`

## 使用例

### python

```bash
import requests
data = {'token': '...', 'content': '...'}
requests.post('http://127.0.0.1:8080/report', json=data)
```

### curl

```bash
curl -L -X POST \
     -d '{"token": "...", "content": "..."}' \
     -H "Content-Type: application/json" \
     -- http://127.0.0.1:8080/report
```

### todo

- [x] 支持设置消息模板
