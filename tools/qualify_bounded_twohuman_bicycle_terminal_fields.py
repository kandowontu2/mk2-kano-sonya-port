"""Both actor observations include the terminal field before host exit."""
import inspect
import qualify_bounded_twohuman_bicycle_command as previous

def main():
    source=inspect.getsource(previous.main)
    source=source.replace("'command_check.json'","'terminal_fields_command_check.json'")
    assert source.count('840')==3;source=source.replace('840','842')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::terminal_actor_fields','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
