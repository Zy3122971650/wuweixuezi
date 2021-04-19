import core


def main():
    wuweixuezi = core.wuweixuezi(server_chan_key=None)
    db = core.dynamodb(region_name=None, aws_access_key_id=None,
                       aws_secret_access_key=None)

    items = db.read_all_user_info()
    count = 0
    for data in items:
        wuweixuezi.task_start(data['id_number'], data['phone_number'],
                              data['password'], data['school_code'], data['style'])
        count += 1
    wuweixuezi.server_chan(count)


main()
