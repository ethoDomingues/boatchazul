import base64

from flask import g
from flask import request
from flask import jsonify
from flask import abort
from flask import render_template


from app.views.auth.utils import auth_manager
from app.model.tables.cdn import Cdn


class CDNFunctions:

    @classmethod
    @auth_manager( required=True )
    def get_form(cls): return render_template("cdn/cdn.html")

    @classmethod
    @auth_manager
    def get_all(cls): return jsonify([ c.to_dict() for c in Cdn.query.all() ])

    @classmethod
    @auth_manager(require=False)
    def get(cls, cdn:str,filename:str):
        cdn = base64.urlsafe_b64decode(cdn.encode()).decode()
        f:Cdn = g.db.tables.getObjectById(cdn, code_error=404, filename=filename )
        return f.body, 200, {"Content-Type": f.headers["Content-Type"]}

    @classmethod
    @auth_manager( required=True )
    def post(cls):
        files = request.files.getlist("files")
        if cls.saveFile(files): 
            g.db.session.commit()
            return "", 204
        abort(500)

    @classmethod
    @auth_manager( required=True )
    def delete(cls, cdn):
        f:Cdn = Cdn.query.filter_by(_id=cdn).first()
        if f:
            g.db.session.delete(f)
            g.db.session.commit()

            return "", 204
        abort(404)
    
    @classmethod
    def saveFile(cls, files):
        fs = []
        if not isinstance(files, list): files = [files]
        for f in files:
            fs.append(Cdn(
                        body = f.stream.read(),
                        owner = g.user.id,
                        headers = {k:v for k,v in f.headers.items()},
                        filename = f.filename
                    ))
        g.db.session.add_all(fs)
        g.db.session.commit()
        return fs
