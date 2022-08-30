
BOT_USERNAME = "dumpsterbot"
BOT_EMOJI = ":dumpster-fire:"

ISSUE_TEMPLATE = """{
	"blocks": [
		{
			"type": "section",
			"text": {
				"text": "*Issue:*\n\n```{issue_match}```\n\n*Description:*\n> {description}",
				"type": "mrkdwn"
			},
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Node:*\n {node}"
				},
				{
					"type": "mrkdwn",
					"text": "*Location:*\n `{file_found}` :file_folder:"
				},
				{
					"type": "mrkdwn",
					"text": "*Severity:*\n {severity}"
				},
				{
					"type": "mrkdwn",
					"text": "*Type:*\n {issue_type}}"
				}
			]
		},
		{
			"type": "divider"
		}
	]
}"""

ABOUT_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                ">dumpster - A Slack app that analyzes Mirantis Kubernetes Engine (MKE) support dump logs"
            ),
        },
    }

HELP_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Here is a list of valid commands:\n \
`/dumpster about`: Get a description of the dumpster app\n \
`/dumpster help`: Show help information message\n"
        },
    }

DIVIDER_BLOCK = {"type": "divider"}
    
def bot_message_payload(channel="", blocks=[]):
    return {
        "channel": channel,
        "username": BOT_USERNAME,
        "icon_emoji": BOT_EMOJI,
        "blocks": blocks
        }

def get_help_message():
    return {"blocks":[HELP_BLOCK]}
    
def get_about_message():
    return {"blocks":[ABOUT_BLOCK]}

