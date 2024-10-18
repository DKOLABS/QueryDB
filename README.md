# Splunk Detection as Code Aid

## Exporting Data

### Saved Searches

#### Splunk Searches
```
| rest /services/saved/searches
| table title, search, owner, eai:acl.app, is_scheduled, cron_schedule
```

#### curl
```bash
curl -k -u <username>:<password> https://<splunk_server>:<management_port>/services/saved/searches -d output_mode=json
```

### Lookup Tables

#### Splunk Search
```
| rest /services/data/lookup-table-files
```

#### curl
```bash
curl -k -u <username>:<password> https://<splunk_server>:<management_port>/services/data/lookup-table-files -d output_mode=json
```