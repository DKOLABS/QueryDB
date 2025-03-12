# Splunk Detection as Code Aid

## Exporting Data

### Saved Searches

#### Splunk Searches
```
| rest splunk_server=local count=0 /services/saved/searches
| fields - auto_summarize.*, dispatch.*, display.*
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