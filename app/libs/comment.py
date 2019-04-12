from app.models import Comment, comment_actions
from app.libs import archived_comment as archivedcommentlib
from app.libs import comment_action_log as commentactionloglib


def create(id, commenter, editors_pick, asset, content, ip_address, parent, created):
    comment = Comment.create(
        id=id,
        commenter=commenter,
        editors_pick=editors_pick,
        asset=asset,
        content=content,
        ip_address=ip_address,
        parent=parent,
        created=created
    )
    return comment.id


def get(id):
    comment = Comment.select().where(Comment.id == id).first()
    return comment.to_dict() if comment else None


def list_(page=1, size=20):
    comments = Comment.select().order_by(Comment.created.desc()).paginate(page, size)
    return [comment.to_dict() for comment in comments]


def update(id, mod_data):
    updatables = ('editors_pick',)
    update_dict = dict((k, v) for (k, v) in list(mod_data.items()) if k in updatables)
    Comment.update(**update_dict).where(Comment.id == id).execute()
    if update_dict.get('editors_pick'):
        commentactionloglib.create(
            comment=id,
            action=comment_actions.picked.value,
            actor=0
        )


def exists(id):
    comment = Comment.select().where(Comment.id == id).first()
    return bool(comment)


def delete(id):
    Comment.delete().where(Comment.id == id).execute()


def archive(id):
    comment = get(id)
    delete(id)
    return archivedcommentlib.create(**comment)


def get_comments_by_asset(asset, parent=0, last_comment=None, limit=None):
    where = [Comment.asset == asset, Comment.parent == parent]
    if parent == 0:  # Top Level Comments(Latest First)
        if last_comment is not None:
            where.append(Comment.id < last_comment)
        order = Comment.id.desc()
    else:  # Second Level Comments fetch(Oldest First)
        if last_comment is not None:
            where.append(Comment.id > last_comment)
        order = Comment.id.asc()

    comments = Comment.select().where(*where).order_by(order)
    if limit:
        comments = comments.limit(limit)

    return [comment.to_dict() for comment in comments]
