import json
from flask import Flask


class Config(Flask):

    def __init__(self, env:str="production"):
        cfg = self.load_cfg(env)
        Flask.__init__(self, **cfg["app_cfg"])
        self.config.from_mapping(cfg["cfg"])

    
    def load_cfg(self, env:str="production") -> dict:
        cfg:dict = {
            "app_cfg":{},
            "cfg":{},
        }
        with open("app.js",) as f:
            cfg_list = ["development", "testing", "production" ]
            if not env: raise ValueError
            if env not in cfg_list: raise ValueError
            cfgs:dict = json.load(f)[0]
            cfg:dict = cfgs.get(env, {})
            def_cfg:dict = cfgs.get("default", {})
            
            for k,v in def_cfg["app_cfg"].items():
                if k not in cfg["app_cfg"]: cfg["app_cfg"][k] = v

            for k,v in def_cfg["cfg"].items():
                if k not in cfg["cfg"]: cfg["cfg"][k] = v
                
        return {
            "app_cfg":
                {
                    "root_path": cfg["app_cfg"].get("root_path", None),
                    "import_name": cfg["app_cfg"].get("import_name", "app"),
                    "static_host": cfg["app_cfg"].get("static_host", None),
                    "host_matching": cfg["app_cfg"].get("host_matching", False),
                    "static_folder": cfg["app_cfg"].get("static_folder", "static"),
                    "instance_path": cfg["app_cfg"].get("instance_path", None),
                    "template_folder": cfg["app_cfg"].get("template_folder", "templates"),
                    "static_url_path": cfg["app_cfg"].get("static_url_path", None),
                    "subdomain_matching": cfg["app_cfg"].get("subdomain_matching", False),
                    "instance_relative_config": cfg["app_cfg"].get("instance_relative_config", False),
                },
            "cfg": cfg["cfg"]
        }