import app.libs.debug as debughelpers
import app.libs.asset_request as arlib
import app.libs.asset as assetlib
import app.libs.pending_comment as pclib
import app.libs.rejected_comment as rclib
import app.libs.comment as commentlib
import app.libs.comment_action_log as actionlog
import app.libs.member as memberlib
import app.libs.publication as publicationlib
import apphelpers.sessions as sessionlib


def setup_routes(factory):

    factory.get('/echo/{word}')(debughelpers.echo)
    factory.get('/whoami')(sessionlib.whoami)

    ar_handlers = (arlib.list_, arlib.create, None, arlib.get, arlib.update, None)
    factory.map_resource('/publications/{pub_id}/assetrequests/', handlers=ar_handlers)
    factory.post('/publications/{pub_id}/assetrequests/{id}/approve')(arlib.approve)
    factory.post('/publications/{pub_id}/assetrequests/{id}/reject')(arlib.reject)
    factory.post('/publications/{pub_id}/assetrequests/{id}/cancel')(arlib.cancel)

    asset_handlers = (assetlib.list_, arlib.create_and_approve, None, assetlib.get, None, None)
    factory.map_resource('/publications/{pub_id}/assets/', handlers=asset_handlers)
    factory.get('/publications/{pub_id}/assets/{id}/comments/count')(assetlib.get_comments_count)
    factory.get('/publications/{pub_id}/assets/{id}/replies')(assetlib.get_replies)
    factory.get('/publications/{pub_id}/assets/{id}/meta')(assetlib.get_meta)
    factory.get('/publications/{pub_id}/assets/meta')(assetlib.get_assets_meta)

    comment_handlers = (commentlib.list_, None, None, commentlib.get, commentlib.update, None)
    factory.map_resource('/publications/{pub_id}/comments/', handlers=comment_handlers)

    actionlog_handlers = (None, actionlog.create, None, None, None, None)
    factory.map_resource('/actionlog/comments/', handlers=actionlog_handlers)
    factory.get('/actionlog/comments/{comment_id}')(actionlog.list_by_comment)

    factory.get('/publications/')(publicationlib.list_)
    factory.get('/publications/{pub_id}/assets')(publicationlib.get_assets_with_comment_stats)

    pc_handlers = (pclib.list_, None, None, pclib.get, None, None)
    factory.map_resource('/publications/{pub_id}/comments/pending/', handlers=pc_handlers)

    factory.post('/publications/{pub_id}/comments/pending/{id}/approve')(pclib.approve)
    factory.post('/publications/{pub_id}/comments/pending/{id}/reject')(pclib.reject)
    factory.get('/publications/{pub_id}/comments/rejected/')(rclib.list_)
    factory.post('/publications/{pub_id}/comments/rejected/{id}/revert')(rclib.revert)

    member_handlers = (memberlib.list_, None, None, None, memberlib.update, None)
    factory.map_resource('/users/', handlers=member_handlers)

    factory.post('/publications/{pub_id}/assets/{id}/stop')(assetlib.stop)
    factory.post('/publications/{pub_id}/assets/{id}/restart')(assetlib.restart)
