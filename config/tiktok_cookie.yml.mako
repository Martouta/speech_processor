<%!
    import os

    def s_v_web_id():
        return os.getenv('TIKTOK_COOKIE_S_V_WEB_ID', 'verify_kjf974fd_y7bupmR0_3uRm_43kF_Awde_8K95qt0GcpBk')
    
    def tt_webid():
        return os.getenv('TIKTOK_COOKIE_TT_WEBID', '6913027209393473025')
%>

development:
  s_v_web_id: ${ s_v_web_id() }
  tt_webid: ${ tt_webid() }

production:
  s_v_web_id: ${ s_v_web_id() }
  tt_webid: ${ tt_webid() }

test:
  s_v_web_id: ${ s_v_web_id() }
  tt_webid: ${ tt_webid() }
