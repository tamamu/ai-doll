WIP

# AI Doll

This is a desktop mascot equipped with dialogue system.

It separates body and AI, they communicate by IPC (interprocess communication.)

Conversation is rule-based, however the emotion affect responses.


### The role of each file and folder

+ body.py  
    Express the doll's body.

+ recognition.py  
    Recognize the text the doll listened.

+ dialogue.json  
    Response sample for dialogue.

+ settings.json  
    App's Settings file. User's path is `$HOME/.config/ai-doll/settings.json`.  
	The format is as below.  
	```
    {
        "init_style": "body",
        "port": 45912,
        "model": "model-name",
        "font": "sans"
    }
    ```

+ models/  
    Put model data directories. User's path is `$HOME/.config/ai-doll/models/`.

+ models/modelname/  
    A model data directory.

+ models/modelname/model  
    A Model data. Each image is found into same directory.  
	The format is as below.  
    ```
    {
        "type": "image",
        "body": "body-image-name",
        "badge": "badge-image-name"
    }
    ```
