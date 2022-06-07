from flask import g
from flask import request
from flask import jsonify
from flask import abort


from app.model.tables.post import Post
from app.model.tables.post import PRIVACITY_DATA

from app.views.auth.utils import auth_manager

from app.views.cdn.functions import CDNFunctions


class POSTSFunctions:

    @classmethod
    @auth_manager(require=True)
    def post(cls, *args, **kwargs):
        data = {}
        payload = request.form
        images = request.files.getlist("images")
        if not payload: payload = request.get_json(silent=True) or {}
        if not images and not payload: abort(400)

        if payload.get("profile") and not images: abort(400)

        if payload.get("content"): data["content"] = payload["content"]
        if payload.get("privacity") is None: abort(401)
        
        priv = payload.get("privacity")

            
        if PRIVACITY_DATA.get(priv):
            data["privacity"] = priv
        else:
            gh = g.db.tables.GroupHook.query.filter_by(_user=g.user.id, _group=priv).first()
            if gh is None: abort(400)
            data["privacity"] = gh.group.id

        if payload.get("shared"):
            images = None
            p = g.db.tables.getObjectById(payload["shared"])
            if p is None: abort(400)
            p_sh = p.shared
            
            if p_sh is None: data["shared"] = p
            else: data["shared"] = p_sh
        
        if images:
            images = CDNFunctions.saveFile(images)
            data["pictures"] = images
        
            
        data["user"] =  g.user
        p = Post(**data)
        g.db.session.add(p)        
        g.db.session.commit()
        if payload.get("profile"):
            g.user.profile = p
            g.db.session.commit()
                
        return jsonify(p.to_dict())
        

    @classmethod
    @auth_manager(require=True)
    def get_list(cls, *args, **kwargs): return jsonify({ "posts": [ p.to_dict() for p in Post.query.filter_by(deleted=0).all() ] })
    
    @classmethod
    @auth_manager()
    def get_all(cls, *args, **kwargs): return jsonify([ p.to_dict() for p in Post.query.all() ])


    @classmethod
    def multiple(cls,*args, **kwargs):
        match request.method:
            case "GET": return cls.get( *args, **kwargs )
            case "PUT": return cls.put( *args, **kwargs )
            case "DELETE": return cls.delete( *args, **kwargs )
            case _: return abort(405)
    
    @classmethod
    @auth_manager()
    def get(cls, post:str, *args, **kwargs): return g.db.tables.getObjectById(post, code_error=404).to_dict()

    @classmethod
    @auth_manager( required=True )
    def put(cls, post, *args, **kwargs):
        post = g.db.tables.getObjectById(post, code_error=404)
        payload = request.form
        images = request.files.getlist("images")
        content = payload.get("content")
        privacity = payload.get("privacity")
        delImages = payload.get("delete")


        if not payload: payload = request.get_json(silent=True) or {}
        if not images and content is None and not post.content: abort(400)

        if content is not None: post.content = content
        if privacity is not None: post.privacity = privacity
        
        if delImages:
            p = post.pictures
            for img in p:
                if img.id in delImages:
                    index = post._pictures.index(img.id)
                    p.pop(index)
                    profile = g.db.tables.Profile.query.filter_by(user=g.user.id, post=post.id, img=img.id).first()
                    if profile: g.db.session.delete(profile)
                    g.db.session.delete(img)
            post.pictures = p # necessario para atualizar esse field no db
                    
        if images:
            imgs = [f.id for f in CDNFunctions.saveFile(images)]

            if post._pictures:
                post._pictures =  post._pictures + imgs 
            else: post._pictures = imgs
        
            
        g.db.session.add(post)
        g.db.session.commit()
                
        return jsonify(**post.to_dict())
        
    

    @classmethod
    @auth_manager( required=True )
    def delete(cls, post:str, *args, **kwargs):
        post = g.db.tables.getObjectById(post, code_error=404)
        if post._user != g.user.id: abort(401)
        post.self_delete()
        return "", 204
