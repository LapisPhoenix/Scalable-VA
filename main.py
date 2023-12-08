import os
from ai import VoiceAssistant


va = VoiceAssistant(name='Computer Jim', activation_keyword='computer')


for file in os.listdir('commands'):
    if file.endswith('.py'):
        va.load_command(f'commands/{file}')


va.run()
