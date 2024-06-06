

'/wechat/banners/home-page?' +
'latitude=31.221139907836914&' +
'longitude=121.5440902709961&' +
'type=BOTTLE_TASK1717687955957VUUPRiNAUexDcr3Wypcjxw==' +
'apyuc3#7%m4*'

T = '/wechat/my-benefits/count'
O.P.getSignature(T, c.toString());
        34483: function(o, G, e) {
            "use strict";
            e.d(G, {
                P: function() {
                    return c
                }
            });
            var i = e(77886)
              , t = e(33661)
              , s = e(12742)
              , r = e(80234)
              , a = e(41032)
              , O = e(49732)
              , m = e.n(O)
              , u = e(46580)
              , d = e(92954)
              , I = e.n(d)
              , z = e(81354)
              , N = e.n(z)
              , T = e(22057)
              , c = function() {
                function j() {
                    (0,
                    t.Z)(this, j)
                }
                return (0,
                s.Z)(j, null, [{
                    key: "getSignature",
                    value: function() {
                        var n = (0,
                        i.Z)(m().mark(function A() {
                            var y, C, g, b, S, w, K = arguments;
                            return m().wrap(function(Z) {
                                for (; ; )
                                    switch (Z.prev = Z.next) {
                                    case 0:
                                        if (y = Date.now(),
                                        !((0,
                                        a.Z)(this, j, D) && (0,
                                        a.Z)(this, j, p) && (0,
                                        a.Z)(this, j, E) > y)) {
                                            Z.next = 5;
                                            break
                                        }
                                        C = (0, a.Z)(this, j, D) + "apyuc3#7%m4*",
                                        Z.next = 18;
                                        break;
                                    case 5:
                                        return Z.prev = 5,
                                        Z.next = 8,
                                        (0,
                                        T.Fr)((0,
                                        d.getUserCryptoManager)().getLatestUserKey)();
                                    case 8:
                                        g = Z.sent,
                                        (0,
                                        r.Z)(this, j, E, g.expireTime),
                                        (0,
                                        r.Z)(this, j, p, g.version),
                                        (0,
                                        r.Z)(this, j, D, g.encryptKey),
                                        C = (0,
                                        a.Z)(this, j, D) + "apyuc3#7%m4*",
                                        Z.next = 18;
                                        break;
                                    case 15:
                                        Z.prev = 15,
                                        Z.t0 = Z.catch(5),
                                        u.kg.error("getUserCryptoManager:", "not get key");
                                    case 18:
                                        for (b = K.length,
                                        S = new Array(b),
                                        w = 0; w < b; w++)
                                            S[w] = K[w];
                                        return S.length && (C = S.reduce(function(B, H) {
                                            return B + H
                                        }) + C),
                                        Z.abrupt("return", {
                                            signature: (0, z.SHA256)(C).toString(z.enc.Hex),
                                            version: (0, a.Z)(this, j, p),
                                            expireTime: (0, a.Z)(this, j, E)
                                        });
                                    case 21:
                                    case "end":
                                        return Z.stop()
                                    }
                            }, A, this, [[5, 15]])
                        }));
                        function M() {
                            return n.apply(this, arguments)
                        }
                        return M
                    }()
                }]),
                j
            }()
              , E = {
                writable: !0,
                value: 0
            }
              , p = {
                writable: !0,
                value: 0
            }
              , D = {
                writable: !0,
                value: ""
            }
        },


function u() {
    return u = (0,
        t.Z)(r().mark(function N(T) {
            var c, E, p, D;
            return r().wrap(function(n) {
                for (; ; )
                    switch (n.prev = n.next) {
                    case 0:
                        return c = Date.now(),
                            n.next = 3,
                            O.P.getSignature(T, c.toString());
                        case 3:
                            return E = n.sent, p = E.version, D = E.signature, n.abrupt("return", {
                                SV: p,
                                "x-sg-timestamp": c.toString(),
                                "x-sg-signature": D
                            });case 7:case "end":return n.stop()
                }
                }, N)
        })),
        u.apply(this, arguments)
}