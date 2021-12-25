import click, time
from pyfiglet import Figlet
from halo import Halo
from ipcqueue import posixmq
import signal, pickle
from multiprocessing import shared_memory
import os

def pass_handler(signal, frame):
    pass


def execute_command(command_type, parameters):
    pid = os.getpid()
    
    message_queue = posixmq.Queue('/doc-phi-listener-queue')
    shm_client = shared_memory.SharedMemory(name='shm_'+str(pid), create=True, size=4096)
    
    request = (command_type, parameters, pid)
    message_queue.put(request)
    
    signal.signal(signal.SIGCONT, pass_handler)
    signal.pause()
    
    response = pickle.loads(shm_client.buf)
    
    message_queue.close()
    shm_client.close()
    shm_client.unlink()
    
    return response


@click.group()
def main():
    f = Figlet(font='larry3d')
    click.secho(f.renderText('doc-phi'), fg='green')
    

@main.command()
def add():
    name = click.prompt(click.style('[?] Name', fg='blue'), type=str)
    path = click.prompt(click.style('[?] Path', fg='blue'), type=str)
    extension = click.prompt(click.style('[?] Type (txt/html/docx/pptx)', fg='blue'), type=str)
    tags = []
    
    if click.confirm(click.style('[Q] Do you want to add tags?', fg='yellow')):
        click.secho('[I] Add space separated tags', fg='yellow')
        tags = click.prompt(click.style('[?] Tags', fg='blue'), type=str)
        tags = tags.split(' ')
    
    parameters = {
        'name': name, 
        'path': path,
        'extension': extension,
        'tags': tags
    }
    
    spinner = Halo(text='Adding file to the database', spinner='dots')
    
    spinner.start()
    response = execute_command(1, parameters)
    spinner.stop()

    click.secho('[✓]: Added file', fg='green') 
    
    
@main.command()
@click.option('--query', '-q', help='Search query')
def search(query):
    parameters = {
        'query': query
    }
    
    spinner = Halo(text='Searching...', text_color='yellow', spinner='dots')
    
    spinner.start()
    response = execute_command(2, parameters)
    spinner.stop()

    click.secho('[✓]: Search Results -', fg='green')  
    for idx, val in enumerate(response):
        click.echo('\n')
        click.echo(str(idx + 1) + '. File Name - ' + val['file_name'])
        click.echo('\tTags - ' + ', '.join(str(x) for x in val['tags']))
    
    
@main.command()
@click.option('--file', '-f', help='Name of the file')
def tags(file):
    parameters = {
        'name': file
    }
    
    spinner = Halo(text='Retrieving tags...', text_color='yellow', spinner='dots')
    
    spinner.start()
    response = execute_command(3, parameters)
    spinner.stop()

    click.echo('\n')
    if len(response) == 0:
        click.secho('[I]: No tags assigned to this file', fg='yellow')
    else:    
        click.secho('[✓]: Assigned tags -', fg='green') 
        click.echo(', '.join(str(x) for x in response))
    click.echo('\n')
    
    
if __name__ == "__main__":
    main()