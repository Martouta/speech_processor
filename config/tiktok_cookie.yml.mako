<%!
    import os
    def s_v_web_id():
        return os.getenv('TIKTOK_COOKIE_S_V_WEB_ID')
%>

development:
  s_v_web_id: ${ s_v_web_id() }

production:
  s_v_web_id: ${ s_v_web_id() }

test:
  s_v_web_id: ${ s_v_web_id() }
