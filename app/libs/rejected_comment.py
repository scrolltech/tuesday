from app.models import RejectedComment


def create(id, commenter_id, commenter, editors_pick, asset, content, ip_address, parent, created, note):
    comment = RejectedComment.create(
        id=id,
        commenter=commenter,
        commenter_id=commenter_id,
        editors_pick=editors_pick,
        asset=asset,
        content=content,
        ip_address=ip_address,
        parent=parent,
        created=created,
        note=note
    )
    return comment.id


def get(id):
    comment = RejectedComment.select().where(RejectedComment.id == id).first()
    return comment.to_dict() if comment else None


def list_(asset_id=None, page=1, size=20):
    comments = RejectedComment.select().order_by(RejectedComment.created.desc()).paginate(page, size)
    if asset_id:
        comments = comments.where(RejectedComment.asset == asset_id)
    return [comment.to_dict() for comment in comments]


def exists(id):
    comment = RejectedComment.select().where(RejectedComment.id == id).first()
    return bool(comment)
