import logging
import dumpsterbot
import os, re, json
import zipfile, tarfile
from requests import get
from requests import HTTPError
from time import perf_counter
from slack_bolt import App
from slack_sdk.web import WebClient
from slack_bolt.adapter.socket_mode import SocketModeHandler

try:
    SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
    SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']
except KeyError:
    logging.critical(" Slack token environment variables not set! Cannot start.")
    exit(1)

app = App(token=SLACK_BOT_TOKEN)

def read_dump_files(files):
    logging.debug(f"starting read of dump file(s): {files}")
    for file in files:
        if file.get('filetype') == 'zip':
            return
        else:
            try:
                with tarfile.open('../cache/' + list(file.keys())[0], mode='r|gz') as tar:
                    tar_files = [tarinfo.name for tarinfo in tar]
                    logging.debug(f"reading tar/gzip found: {tar_files}")
            except tarfile.TarError as err:
                return

def download_dump_files(files: list, token: str):
    downloaded_files = []
    for file in files:
        filename, filetype = file['name'], file['filetype']
        url = file['url_private']
        headers = {"Authorization": f"Bearer {token}"}
        try:
            start_time = perf_counter()
            r = get(url, headers=headers, stream=True, timeout=3)
            r.raise_for_status()
            with open("../cache/" + filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=2097152):
                    f.write(chunk)
            end_time = perf_counter()
            logging.debug(f"download and write of file {filename} completed in {float(end_time - start_time):.3f} seconds")
            downloaded_files.append({filename: filetype})
        except HTTPError as err:
            logging.error(f"file download failed: {filename}: {err}")
            continue
    return read_dump_files(downloaded_files)

@app.event('app_mention')
def handle_mention(event, client: WebClient):
    logging.debug(json.dumps(event))
    channel, user = event.get('channel'), event.get('user')

    try:
        files_metadata = event['files']
        dump_files = []
        for file in files_metadata:
            if file['filetype'] not in ['zip', 'gzip', 'binary']:
                continue
            elif re.fullmatch("^docker-support-.*.(zip|tgz|tar.gz)$", file['name']) is not None:
                dump_files.append(file)
    
        logging.debug("support dump file(s) found: " + json.dumps(dump_files))
        if not dump_files:
            raise KeyError
        else:
            return download_dump_files(dump_files, SLACK_BOT_TOKEN)
    except KeyError:
        client.chat_postEphemeral(**dumpsterbot.bot_message_payload(channel=channel),
                text=">No support dump file(s) found in app mention",
                user=user
        )
    return

@app.command('/dumpster')
def handle_command(ack, body):
    logging.debug(json.dumps(body))
    command = body['text'].lower()

    if command == 'about':
        ack(**dumpsterbot.get_about_message())
    else:
        ack(**dumpsterbot.get_help_message())
    return
    
if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-5s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',\
        level=logging.DEBUG
        )
    SocketModeHandler(app, SLACK_APP_TOKEN).start()