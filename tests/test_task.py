# -*- coding: utf-8 -*-
import json
from app.database import model
from app.tasks.tasks import do_webhook_shell
from . import WEBHOOKDATA


def test_do_webhook_shell(create_server, create_webhook, sql):
    server = create_server()
    webhook = create_webhook(server_id=server['id'])
    data = WEBHOOKDATA['github']
    history = model.History(
        status='1',
        webhook_id=webhook['id'],
        data=json.dumps(data)
    )
    sql.add(history)
    sql.commit()
    print(model.History.query.get(history.id))
    # with mock.patch.object(ssh, 'do_ssh_cmd', new=mock_do_ssh_cmd):
    text = 'select * from history where id=:id'
    result = sql.execute(text, {'id': history.id}).fetchone()
    assert result.status == '1'
    do_webhook_shell.apply(args=(webhook['id'], history.id, data)).get()
    result = sql.execute(text, {'id': history.id}).fetchone()
    assert result.status == '5'
