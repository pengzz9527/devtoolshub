import json
with open('/root/.hermes/cron/output/innovation_projects_sent.json', 'r') as f:
    data = json.load(f)
data['projects'].append({
    'name': 'coreyhaines31/marketingskills',
    'url': 'https://github.com/coreyhaines31/marketingskills',
    'date': '2026-09-08',
    'sent_at': '2026-09-08T10:00:00',
    'email_status': 'sent'
})
with open('/root/.hermes/cron/output/innovation_projects_sent.json', 'w') as f:
    json.dump(data, f, indent=2)
print('Dedup file updated successfully')
