
saveSign: function (t, e, a) {
      var i = this;
      w((function (o, n, r, d) {
        var c = {
          unionId: o,
          openId: n,
          userIcon: i.data.headerImg,
          nickName: i.data.nickName,
          isFromWindow: i.data.isFromWindow
        };
        h.compareVersion(I, "2.17.3") >= 0 && (console.log("当前版本号：" + I), (0, s.encryptData)(c).then((function (o) {
          var n = o.data,
            s = o.version;
          c.version = s,
          c.encryptedData = n,
          console.log("签到加密数据：" + JSON.stringify(c) + " ;version:" + s),
          DesktopReward(t, e, a, c)
        })).catch((function (t) {
          console.log("签到加密失败：" + t), h.showToast("签到失败，稍后重试", "none")
        })))
      }))
}

function DesktopReward (t, e, a, i) {
      var o = this;
      w((function (n, s, r, d) {
        m({
          url: S + "sign/retrieveDesktopReward",
          data: i,
          header: O,
          method: "POST",
          success: function (i) {
            var n = i.data;
            200 == n.code ? o.gatherAn(t, e, a) : h.showToast(n.msg || "桌面签到失败~", "none")
          }
        })
      }))
}

module.exports = {
    encryptData: function () {
      var e, t = this,
        a = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "",
        c = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {};
      return new Promise((e = r(s.default.mark((function e(r, f) {
        var l, y;
        return s.default.wrap((function (e) {
          for (;;) switch (e.prev = e.next) {
            case 0:
              if (e.prev = 0, !c.encryptKey) {
                e.next = 5;
                break
              }
              e.t0 = {
                encryptKey: c.encryptKey,
                iv: c.iv || ""
              }, e.next = 8;
              break;
            case 5:
              return e.next = 7, n();
            case 7:
              e.t0 = e.sent;
            case 8:
              if (!(l = e.t0).encryptKey) {
                e.next = 16;
                break
              }
              return e.next = 12, u.default.setRoundKey();
            case 12:
              e.sent.success ? (y = i(l.encryptKey, l.iv, a)).encryptedHex ? r && r({
                data: y.encryptedHex,
                version: l.version
              }) : (f && f({
                fail: "encrypt-fail"
              }), (0, o.ev)("page", 2e3, "aes加密失败", "encrypt-fail^" + JSON.stringify(y))) : (f && f({
                fail: "getRoundKey-fail"
              }), (0, o.ev)("page", 2e3, "aes加密失败", "getRoundKey-fail")), e.next = 18;
              break;
            case 16:
              f && f({
                fail: "getLatestUserKey-fail"
              }), (0, o.ev)("page", 2e3, "aes加密失败", "getLatestUserKey-fail^" + JSON.stringify(l));
            case 18:
              e.next = 24;
              break;
            case 20:
              e.prev = 20, e.t1 = e.catch(0), f && f(e.t1), (0, o.ev)("page", 2e3, "aes加密失败", "getLatestUserKey-fail^" + JSON.stringify(e.t1));
            case 24:
            case "end":
              return e.stop()
          }
        }), e, t, [
          [0, 20]
        ])
      }))), function (t, r) {
        return e.apply(this, arguments)
      }))
    }
  };