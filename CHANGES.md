# Microdot change log

**Release 2.3.3** - 2025-07-01

- Handle partial reads in WebSocket class [#294](https://github.com/miguelgrinberg/microdot/issues/294) ([commit](https://github.com/miguelgrinberg/microdot/commit/9bc3dced6c1f582dde0496961d25170b448ad8d7))
- Add SVG to supported mimetypes [#302](https://github.com/miguelgrinberg/microdot/issues/302) ([commit](https://github.com/miguelgrinberg/microdot/commit/1d419ce59bf7006617109c05dc2d6fc6d1dc8235)) (thanks **Ozuba**!)
- Do not silence exceptions that occur in the SSE task ([commit](https://github.com/miguelgrinberg/microdot/commit/654a85f46b7dd7a1e94f81193c4a78a8a1e99936))
- Add Support for SSE responses in the test client ([commit](https://github.com/miguelgrinberg/microdot/commit/f5d3d931edfbacedebf5fdf938ef77c5ee910380))
- Documentation improvements for the `Request` class ([commit](https://github.com/miguelgrinberg/microdot/commit/3dffa05ffb229813156b71e10a85283bdaa26d5e))
- Additional documentation for the `URLPattern` class ([commit](https://github.com/miguelgrinberg/microdot/commit/786e5e533748e1343612c97123773aec9a1a99fc))
- More detailed documentation for route responses ([commit](https://github.com/miguelgrinberg/microdot/commit/dc61470fa959549bb43313906ba6ed9f686babc2))
- Additional documentation on WebSocket and SSE disconnections ([commit](https://github.com/miguelgrinberg/microdot/commit/7c98c4589de4774a88381b393444c75094532550))
- More detailed documentation for `current_user` ([commit](https://github.com/miguelgrinberg/microdot/commit/e146e2d08deddf9b924c7657f04db28d71f34221))
- Add a sub-application example ([commit](https://github.com/miguelgrinberg/microdot/commit/d7a9c535639268e415714b12ac898ae38e516308))

**Release 2.3.2** - 2025-05-08

- Use async error handlers in auth module [#298](https://github.com/miguelgrinberg/microdot/issues/298) ([commit](https://github.com/miguelgrinberg/microdot/commit/d9d7ff0825e4c5fbed6564d3684374bf3937df11))

**Release 2.3.1** - 2025-04-13

- Additional support needed when using `orjson` ([commit](https://github.com/miguelgrinberg/microdot/commit/cd0b3234ddb0c8ff4861d369836ec2aed77494db))

**Release 2.3.0** - 2025-04-12

- Support optional authentication methods ([commit](https://github.com/miguelgrinberg/microdot/commit/f317b15bdbf924007e5e3414e0c626baccc3ede6))
- Catch SSL exceptions while writing the response [#206](https://github.com/miguelgrinberg/microdot/issues/206) ([commit](https://github.com/miguelgrinberg/microdot/commit/e7ee74d6bba74cfd89b9ddc38f28e02514eb1791))
- Use `orjson` instead of `json` if available ([commit](https://github.com/miguelgrinberg/microdot/commit/086f2af3deab86d4340f3f1feb9e019de59f351d))
- Addressed typing warnings from pyright ([commit](https://github.com/miguelgrinberg/microdot/commit/b6f232db1125045d79c444c736a2ae59c5501fdd))

**Release 2.2.0** - 2025-03-22

- Support for `multipart/form-data` requests [#287](https://github.com/miguelgrinberg/microdot/issues/287) ([commit](https://github.com/miguelgrinberg/microdot/commit/11a91a60350518e426b557fae8dffe75912f8823))
- Support custom path components in URLs ([commit #1](https://github.com/miguelgrinberg/microdot/commit/c92b5ae28222af5a1094f5d2f70a45d4d17653d5) [commit #2](https://github.com/miguelgrinberg/microdot/commit/aa76e6378b37faab52008a8aab8db75f81b29323))
- Expose the Jinja environment as `Template.jinja_env` ([commit](https://github.com/miguelgrinberg/microdot/commit/953dd9432122defe943f0637bbe7e01f2fc7743f))
- Simplified urldecode logic ([commit #1](https://github.com/miguelgrinberg/microdot/commit/3bc31f10b2b2d4460c62366013278d87665f0f97) [commit #2](https://github.com/miguelgrinberg/microdot/commit/d203df75fef32c7cc0fe7cc6525e77522b37a289))
- Additional urldecode tests ([commit](https://github.com/miguelgrinberg/microdot/commit/99f65c0198590c0dfb402c24685b6f8dfba1935d))
- Documentation improvements ([commit](https://github.com/miguelgrinberg/microdot/commit/c6b99b6d8117d4e40e16d5b953dbf4deb023d24d))
- Update micropython version used in tests to 1.24.1 ([commit](https://github.com/miguelgrinberg/microdot/commit/4cc2e95338a7de3b03742389004147ee21285621))

**Release 2.1.0** - 2025-02-04

- User login support ([commit](https://github.com/miguelgrinberg/microdot/commit/d807011ad006e53e70c4594d7eac04d03bb08681))
- Basic and token authentication support ([commit](https://github.com/miguelgrinberg/microdot/commit/675c9787974da926af446974cd96ef224e0ee27f))
- Added `local` argument to the `app.mount()` method, to define sub-application specific before and after request handlers ([commit](https://github.com/miguelgrinberg/microdot/commit/fd7931e1aec173c60f81dad18c1a102ed8f0e081))
- Added `Request.url_prefix`, `Request.subapp` and local mounts ([commit](https://github.com/miguelgrinberg/microdot/commit/fd7931e1aec173c60f81dad18c1a102ed8f0e081))
- Added a front end to the SSE example [#281](https://github.com/miguelgrinberg/microdot/issues/281) ([commit](https://github.com/miguelgrinberg/microdot/commit/d487a73c1ea5b3467e23907618b348ca52e0235c)) (thanks **Maxi**!)
- Additional ``app.mount()`` unit tests ([commit](https://github.com/miguelgrinberg/microdot/commit/cd87abba30206ec6d3928e0aabacb2fccf7baf70))

**Release 2.0.7** - 2024-11-10

- Accept responses with just a status code [#263](https://github.com/miguelgrinberg/microdot/issues/263) ([commit #1](https://github.com/miguelgrinberg/microdot/commit/4eac013087f807cafa244b8a6b7b0ed4c82ff150) [commit #2](https://github.com/miguelgrinberg/microdot/commit/c46e4291061046f1be13f300dd08645b71c16635))
- Fixed compressed file content-type assignment [#251](https://github.com/miguelgrinberg/microdot/issues/251) ([commit](https://github.com/miguelgrinberg/microdot/commit/482ab6d5ca068d71ea6301f45918946161e9fcc1)) (thanks **Lukas Kremla**!)
- Better documentation for start_server[#252](https://github.com/miguelgrinberg/microdot/issues/252) ([commit](https://github.com/miguelgrinberg/microdot/commit/0a021462e0c42c249d587a2d600f5a21a408adfc))
- Fix URLs in documentation [#253](https://github.com/miguelgrinberg/microdot/issues/253) ([commit](https://github.com/miguelgrinberg/microdot/commit/5e5fc5e93e11cbf6e3dc8036494e8732d1815d3e)) (thanks **Stanislav Garanzha**!)

**Release 2.0.6** - 2024-06-18

- Add event ID to the SSE implementation [#213](https://github.com/miguelgrinberg/microdot/issues/213) ([commit](https://github.com/miguelgrinberg/microdot/commit/904d5fcaa2d19d939a719b8e68c4dee3eb470739)) (thanks **Hamsanger**!)
- Configurable session cookie options [#242](https://github.com/miguelgrinberg/microdot/issues/242) ([commit](https://github.com/miguelgrinberg/microdot/commit/0151611fc84fec450820d673f4c4d70c32c990a7))
- Improved cookie support in the test client ([commit](https://github.com/miguelgrinberg/microdot/commit/4cb155ee411dc2d9c9f15714cb32b25ba79b156a))
- Cookie path support in session extension and test client ([commit](https://github.com/miguelgrinberg/microdot/commit/6ffb8a8fe920111c4d8c16e98715a0d5ee2d1da3))
- Refactor `Session` class to make it more reusable ([commit](https://github.com/miguelgrinberg/microdot/commit/dea79c5ce224dec7858ffef45a42bed442fd3a5a))
- Use `@functools.wraps` on decorated functions ([commit](https://github.com/miguelgrinberg/microdot/commit/f6876c0d154adcae96098405fb6a1fdf1ea4ec28))
- Removed outdated import from documentation [#216](https://github.com/miguelgrinberg/microdot/issues/216) ([commit](https://github.com/miguelgrinberg/microdot/commit/6b1fd6191702e7a9ad934fddfcdd0a3cebea7c94)) (thanks **Carlo Colombo**!)
- Add roadmap details to readme ([commit](https://github.com/miguelgrinberg/microdot/commit/a0ea439def238084c4d68309c0992b66ffd28ad6))

**Release 2.0.5** - 2024-03-09

- Correct handling of 0 as an integer argument (regression from #207) [#212](https://github.com/miguelgrinberg/microdot/issues/212) ([commit](https://github.com/miguelgrinberg/microdot/commit/d0a4cf8fa7dfb1da7466157b18d3329a8cf9a5df))

**Release 2.0.4** - 2024-02-20

- Do not use regexes for parsing simple URLs [#207](https://github.com/miguelgrinberg/microdot/issues/207) ([commit #1](https://github.com/miguelgrinberg/microdot/commit/38262c56d34784401659639b482a4a1224e1e59a) [commit #2](https://github.com/miguelgrinberg/microdot/commit/f6cba2c0f7e18e2f32b5adb779fb037b6c473eab))
- Added documentation on using alternative uTemplate loaders ([commit](https://github.com/miguelgrinberg/microdot/commit/bf519478cbc6e296785241cd7d01edb23c317cd3))
- Added CircuitPython builds ([commit](https://github.com/miguelgrinberg/microdot/commit/e44c271bae88f4327d3eda16d8780ac264d1ebab))

**Release 2.0.3** - 2024-01-07

- Add a limit to WebSocket message size [#193](https://github.com/miguelgrinberg/microdot/issues/193) ([commit](https://github.com/miguelgrinberg/microdot/commit/5d188e8c0ddef6ce633ca702dbdd4a90f2799597))
- Pass keyword arguments to thread executor in the correct way [#195](https://github.com/miguelgrinberg/microdot/issues/195) ([commit](https://github.com/miguelgrinberg/microdot/commit/6712c47400d7c426c88032f65ab74466524eccab))
- Update uasyncio library used in tests to include new TLS support ([commit](https://github.com/miguelgrinberg/microdot/commit/c8c91e83457d24320f22c9a74e80b15e06b072ca))
- Documentation improvements ([commit](https://github.com/miguelgrinberg/microdot/commit/b80b6b64d02d21400ca8a5077f5ed1127cc202ae))

**Release 2.0.2** - 2023-12-28

- Support binary data in the SSE extension ([commit](https://github.com/miguelgrinberg/microdot/commit/1fc11193da0d298f5539e2ad218836910a13efb2))
- Upgrade micropython tests to use v1.22 + initial CircuitPython testing work ([commit](https://github.com/miguelgrinberg/microdot/commit/79452a46992351ccad2c0317c20bf50be0d76641))
- Improvements to migration guide ([commit](https://github.com/miguelgrinberg/microdot/commit/84842e39c360a8b3ddf36feac8af201fb19bbb0b))
- Remove spurious async in documentation example [#187](https://github.com/miguelgrinberg/microdot/issues/187) ([commit](https://github.com/miguelgrinberg/microdot/commit/ad368be993e2e3007579f1d3880e36d60c71da92)) (thanks **Tak Tran**!)

**Release 2.0.1** - 2023-12-23

- Addressed some inadvertent mistakes in the template extensions ([commit](https://github.com/miguelgrinberg/microdot/commit/bd18ceb4424e9dfb52b1e6d498edd260aa24fc53))

**Release 2.0.0** - 2023-12-22

- Major redesign [#186](https://github.com/miguelgrinberg/microdot/issues/186) ([commit](https://github.com/miguelgrinberg/microdot/commit/20ea305fe793eb206b52af9eb5c5f3c1e9f57dbb))
    - Code reorganization as a `microdot` package
    - Asyncio is now the core implementation
    - New support for Server-Sent Events (SSE)
    - Several extensions redesigned
    - Support for "partitioned" cookies
    - [Cross-compiling and freezing](https://microdot.readthedocs.io/en/stable/freezing.html) guidance
    - A [Migration Guide](https://microdot.readthedocs.io/en/stable/migrating.html) to help transition to version 2 from older releases

**Release 1.3.4** - 2023-11-08

- Handle change in `wait_closed()` behavior in Python 3.12 [#177](https://github.com/miguelgrinberg/microdot/issues/177) ([commit](https://github.com/miguelgrinberg/microdot/commit/5550b20cdd347d59e2aa68f6ebf9e9abffaff9fc))
- Added missing request argument in some documentation examples [#163](https://github.com/miguelgrinberg/microdot/issues/163) ([commit](https://github.com/miguelgrinberg/microdot/commit/744548f8dc33a72512b34c4001ee9c6c1edd22ee))
- Fix minor documentation typos [#161](https://github.com/miguelgrinberg/microdot/issues/161) ([commit](https://github.com/miguelgrinberg/microdot/commit/2e4911d10826cbb3914de4a45e495c3be36543fa)) (thanks **Andy Piper**!)

**Release 1.3.3** - 2023-07-16

- Handle query string arguments without value [#149](https://github.com/miguelgrinberg/microdot/issues/149) ([commit](https://github.com/miguelgrinberg/microdot/commit/3554bc91cb1523efa5b66fe3ef173f8e86e8c2a0))
- Support empty responses with ASGI adapter ([commit](https://github.com/miguelgrinberg/microdot/commit/e09e9830f43af41d38775547637558494151a385))
- Added CORS extension to Python package ([commit](https://github.com/miguelgrinberg/microdot/commit/304ca2ef6881fe718126b3e308211e760109d519))
- Document access to WSGI and ASGI attributes [#153](https://github.com/miguelgrinberg/microdot/issues/153) ([commit](https://github.com/miguelgrinberg/microdot/commit/d99df2c4010ab70c60b86ab334d656903e04eb26))
- Upgrade micropython tests to use v1.20 ([commit](https://github.com/miguelgrinberg/microdot/commit/e0f0565551966ee0238a5a1819c78a13639ad704))

**Release 1.3.2** - 2023-06-13

- In ASGI, return headers as strings and not binary [#144](https://github.com/miguelgrinberg/microdot/issues/144) ([commit](https://github.com/miguelgrinberg/microdot/commit/e92310fa55bbffcdcbb33f560e27c3579d7ac451))
- Incorrect import in `static_async.py` example ([commit](https://github.com/miguelgrinberg/microdot/commit/c07a53943508e64baea160748e67efc92e75b036))

**Release 1.3.1** - 2023-05-21

- Support negative numbers for int path components [#137](https://github.com/miguelgrinberg/microdot/issues/137) ([commit](https://github.com/miguelgrinberg/microdot/commit/a0dd7c8ab6d681932324e56ed101aba861a105a0))
- Use a more conservative default for socket timeout [#130](https://github.com/miguelgrinberg/microdot/issues/130) ([commit](https://github.com/miguelgrinberg/microdot/commit/239cf4ff37268a7e2467b93be44fe9f91cee8aee))
- More robust check for socket timeout error code [#106](https://github.com/miguelgrinberg/microdot/issues/106) ([commit](https://github.com/miguelgrinberg/microdot/commit/efec9f14be7b6f3451e4d1d0fe7e528ce6ca74dc))
- WebSocket error when handling PING packet [#129](https://github.com/miguelgrinberg/microdot/issues/129) ([commit](https://github.com/miguelgrinberg/microdot/commit/87cd098f66e24bed6bbad29b1490a129e355bbb3))
- Explicitly set UTF-8 encoding for HTML files in examples [#132](https://github.com/miguelgrinberg/microdot/issues/132) ([commit](https://github.com/miguelgrinberg/microdot/commit/f81de6d9582f4905b9c2735d3c639b92d7e77994))

**Release 1.3.0** - 2023-04-08

- Cross-Origin Resource Sharing (CORS) extension [#45](https://github.com/miguelgrinberg/microdot/issues/45) ([commit](https://github.com/miguelgrinberg/microdot/commit/67798f7dbffb30018ab4b62a9aaa297f63bc9e64))
- Respond to `HEAD` and `OPTIONS` requests ([commit](https://github.com/miguelgrinberg/microdot/commit/6a31f89673518e79fef5659c04e609b7976a5e34))
- Tolerate slightly invalid formats in query strings [#126](https://github.com/miguelgrinberg/microdot/issues/126) ([commit](https://github.com/miguelgrinberg/microdot/commit/a1b061656fa19dae583951596b0f1f0603652a56))
- Support compressed files in `send_file()` [#93](https://github.com/miguelgrinberg/microdot/issues/93) ([commit](https://github.com/miguelgrinberg/microdot/commit/daf1001ec55ab38e6cdfee4931729a3b7506858b))
- Add `max_age` argument to `send_file()` ([commit](https://github.com/miguelgrinberg/microdot/commit/e684ee32d91d3e2ab9569bb5fd342986c010ffeb))
- Add `update()` method to `NoCaseDict` class ([commit](https://github.com/miguelgrinberg/microdot/commit/ea6766cea96b756b36ed777f9c1b6a6680db09ba))
- Set exit code to 1 for failed MicroPython test runs ([commit](https://github.com/miguelgrinberg/microdot/commit/a350e8fd1e55fac12c9e5b909cfa82d880b177ef))

**Release 1.2.4** - 2023-03-03

- One more attempt to correct build issues ([commit](https://github.com/miguelgrinberg/microdot/commit/cb39898829f4edc233ab4e7ba3f7ef3c5c50f196))

**Release 1.2.3** - 2023-03-03

- Corrected a problem with previous build.

**Release 1.2.2** - 2023-03-03

- Add a socket read timeout to abort incomplete requests [#99](https://github.com/miguelgrinberg/microdot/issues/99) ([commit](https://github.com/miguelgrinberg/microdot/commit/d0d358f94a63f8565d6406feff0c6e7418cc7f81))
- More robust timeout handling [#106](https://github.com/miguelgrinberg/microdot/issues/106) ([commit](https://github.com/miguelgrinberg/microdot/commit/4d432a7d6cd88b874a8b825fb62891ed22881f74))
- Add @after_error_handler decorator [#97](https://github.com/miguelgrinberg/microdot/issues/97) ([commit](https://github.com/miguelgrinberg/microdot/commit/fcaeee69052b5681706f65b022e667baeee30d4d))
- Return headers as lowercase byte sequences as required by ASGI ([commit](https://github.com/miguelgrinberg/microdot/commit/ddb3b8f442d3683df04554104edaf8acd9c68148))
- Async example of static file serving ([commit](https://github.com/miguelgrinberg/microdot/commit/680cd9c023352f0ff03d67f1041ea174b7b7385b))
- Fixing broken links to examples in documentation [#101](https://github.com/miguelgrinberg/microdot/issues/101) ([commit](https://github.com/miguelgrinberg/microdot/commit/c00b24c9436e1b8f3d4c9bb6f2adfca988902e91)) (thanks **Eric Welch**!)
- Add scrollbar to documentation's left sidebar ([commit](https://github.com/miguelgrinberg/microdot/commit/2aa90d42451dc64c84efcc4f40a1b6c8d1ef1e8d))
- Documentation typo [#90](https://github.com/miguelgrinberg/microdot/issues/90) ([commit](https://github.com/miguelgrinberg/microdot/commit/81394980234f24aac834faf8e2e8225231e9014b)) (thanks **William Wheeler**!)
- Add CPU timing to benchmark ([commit](https://github.com/miguelgrinberg/microdot/commit/9398c960752f87bc32d7c4349cbf594e5d678e99))
- Upgrade uasyncio release used in tests ([commit](https://github.com/miguelgrinberg/microdot/commit/3d6815119ca1ec989f704f626530f938c857a8e5))
- Update unittest library for MicroPython ([commit](https://github.com/miguelgrinberg/microdot/commit/ecd84ecb7bd3c29d5af96739442b908badeab804))
- New build of micropython for unit tests ([commit](https://github.com/miguelgrinberg/microdot/commit/818f98d9a4e531e01c0f913813425ab2b40c289d))
- Remove 3.6, add 3.11 to builds ([commit](https://github.com/miguelgrinberg/microdot/commit/dd15d90239b73b5fd413515c9cd4ac23f6d42f67))

**Release 1.2.1** - 2022-12-06

- Error handling invokes parent exceptions [#74](https://github.com/miguelgrinberg/microdot/issues/74) ([commit](https://github.com/miguelgrinberg/microdot/commit/24d74fb8483b04e8abe6e303e06f0a310f32700b)) (thanks **Diego Pomares**!)
- Addressed error when deleting a user session in async app [#86](https://github.com/miguelgrinberg/microdot/issues/86) ([commit](https://github.com/miguelgrinberg/microdot/commit/5a589afd5e519e94e84fc1ee69033f2dad51c3ea))
- Add asyncio file upload example ([commit](https://github.com/miguelgrinberg/microdot/commit/c841cbedda40f59a9d87f6895fdf9fd954f854a2))
- New Jinja and uTemplate examples with Bootstrap ([commit](https://github.com/miguelgrinberg/microdot/commit/211ad953aeedb4c7f73fe210424aa173b4dc7fee))
- Fix typos in documentation [#77](https://github.com/miguelgrinberg/microdot/issues/77) ([commit](https://github.com/miguelgrinberg/microdot/commit/4a9b92b800d3fd87110f7bc9f546c10185ee13bc)) (thanks **Diego Pomares**!)
- Add missing exception argument to error handler example in documentation [#73](https://github.com/miguelgrinberg/microdot/issues/73) ([commit](https://github.com/miguelgrinberg/microdot/commit/c443599089f2127d1cb052dfba8a05c1969d65e3)) (thanks **Diego Pomares**!)

**Release 1.2.0** - 2022-09-25

- Use a case insensitive dict for headers ([commit #1](https://github.com/miguelgrinberg/microdot/commit/b0fd6c432371ca5cb10d07ff84c4deed7aa0ce2e) [commit #2](https://github.com/miguelgrinberg/microdot/commit/a8515c97b030f942fa6ca85cbe1772291468fb0d))
- urlencode() helper function ([commit #1](https://github.com/miguelgrinberg/microdot/commit/672512e086384e808489305502e6ebebcc5a888f) [commit #2](https://github.com/miguelgrinberg/microdot/commit/b133dcc34368853ee685396a1bcb50360e807813))
- Added `request.url` attribute with the complete URL of the request ([commit](https://github.com/miguelgrinberg/microdot/commit/1547e861ee28d43d10fe4c4ed1871345d4b81086))
- Do not log HTTPException occurrences ([commit](https://github.com/miguelgrinberg/microdot/commit/cbefb6bf3a3fdcff8b7a8bacad3449be18e46e3b))
- Cache user session for performance ([commit](https://github.com/miguelgrinberg/microdot/commit/01947b101ebe198312c88d73872e3248024918f0))
- File upload example ([commit](https://github.com/miguelgrinberg/microdot/commit/8ebe81c09b604ddc1123e78ad6bc87ceda5f8597))
- Minor documentation styling fixes ([commit](https://github.com/miguelgrinberg/microdot/commit/4f263c63ab7bb1ce0dd48d8e00f3c6891e1bf07e))

**Release 1.1.1** - 2022-09-18

- Make WebSocket internals consistent between TLS and non-TLS [#61](https://github.com/miguelgrinberg/microdot/issues/61) ([commit](https://github.com/miguelgrinberg/microdot/commit/5693b812ceb2c0d51ec3c991adf6894a87e6fcc7))

**Release 1.1.0** - 2022-09-17

- Websocket support [#55](https://github.com/miguelgrinberg/microdot/issues/55) ([commit](https://github.com/miguelgrinberg/microdot/commit/2399c29c8a45289f009f47fd66438452da93cdab))
- SSL/TLS support ([commit #1](https://github.com/miguelgrinberg/microdot/commit/b61f51f2434465b7a0ee197aabf46e8f99f6e8ad) [commit #2](https://github.com/miguelgrinberg/microdot/commit/fe750feb0373b41cb022521a6a3edf1973847a74))
- Add `abort()` function ([commit](https://github.com/miguelgrinberg/microdot/commit/3c125c43d2e037ce64138e22c1ff4186ea107471))
- Charset handling in Content-Type headers [#60](https://github.com/miguelgrinberg/microdot/issues/60) ([commit](https://github.com/miguelgrinberg/microdot/commit/75725795b45d275deaee133204e400e8fbb3de70))
- Recover from errors writing the response ([commit](https://github.com/miguelgrinberg/microdot/commit/dc7a041ebd30f38b9f6b22c4bbcd61993c43944e))
- Reorganized examples into subdirectories ([commit](https://github.com/miguelgrinberg/microdot/commit/a01fc9c3f070e21e705b8f12ceb8288b0f304569))
- Update tests to use MicroPython 1.19 ([commit](https://github.com/miguelgrinberg/microdot/commit/42b6d6979381d9cd8ccc6ab6e079f12ec5987b80))
- Update MicroPython libraries used by tests ([commit](https://github.com/miguelgrinberg/microdot/commit/e767426228eeacd58886bccb5046049e994c0479))
- Fix links to hello and gpio examples in documentation [#53](https://github.com/miguelgrinberg/microdot/issues/53) ([commit](https://github.com/miguelgrinberg/microdot/commit/ec0f9ba855cca7dd35cddad40c4cb7eb17d8842a)) (thanks **Sterling G. Baird**!)

**Release 1.0.0** - 2022-08-07

- User sessions with signed JWTs ([commit](https://github.com/miguelgrinberg/microdot/commit/355ffefcb2697b30d03359d35283835901f375d6))
- Mount sub-applications ([commit](https://github.com/miguelgrinberg/microdot/commit/cd5b35d86f2bdd2924234d19943b06dbad6db7c0))
- Request-specific `after_request` handlers ([commit](https://github.com/miguelgrinberg/microdot/commit/120abe45ecee3ef215c2201337fcb399d5602d59))
- Render templates with uTemplate ([commit](https://github.com/miguelgrinberg/microdot/commit/54c13295827548a9258a9af914d199f06d8ae5cd))
- Render templates with Jinja ([commit](https://github.com/miguelgrinberg/microdot/commit/7686b2ae38fb980de0de33c1585f430af11e1cdf))
- Test client ([commit](https://github.com/miguelgrinberg/microdot/commit/199d23f2c72356072a32fa7bdc85b094c8a63766))
- Async test client ([commit](https://github.com/miguelgrinberg/microdot/commit/3bcdf4d496630672ed702677b1e22e5364b2b95a))
- Example that serves static files from a directory ([commit](https://github.com/miguelgrinberg/microdot/commit/a3d7772b8a8e49526f895d10af52a4c0568922b2))
- Allow routes to only return a body and headers ([commit](https://github.com/miguelgrinberg/microdot/commit/16f3775fa26ea08600898f6a244d5baabea32813))
- Improved handling of 400 and 405 errors ([commit](https://github.com/miguelgrinberg/microdot/commit/8177b9c7f1c1dfedcd10dcd1562caf6e442d941f))
- Support responses with more than one cookie in WSGI and ASGI extensions ([commit](https://github.com/miguelgrinberg/microdot/commit/e8d16cf3f90270c5cd3fb13168c5cc983708989c))
- Cookie expiration can also be given as a string ([commit](https://github.com/miguelgrinberg/microdot/commit/3a54984b674148b6e590eb989de18c1ff0aa9217))
- Accept POST request with empty body ([commit](https://github.com/miguelgrinberg/microdot/commit/bf3aff6c35982c7dc4a42ae5415933b252cebc0d))
- Add missing asgi module to package ([commit](https://github.com/miguelgrinberg/microdot/commit/7f1e546067d2222fa1499af69a6a697e5b7188be))
- Memory usage comparison and benchmark ([commit](https://github.com/miguelgrinberg/microdot/commit/d090bbf8e2b7ce07c802b06de7ebb29de68d788d))
- Do not use `_thread` for multithreading ([commit](https://github.com/miguelgrinberg/microdot/commit/998c1970586bf5298b6f749460ab88496e429612))
- Getting Started documentation chapter ([commit](https://github.com/miguelgrinberg/microdot/commit/037024320f08e294601d7b4e206b309dc77b1d90))
- Concurrency section added to the documentation ([commit](https://github.com/miguelgrinberg/microdot/commit/2f496db50b3d3629c68178b5915454cf1d87bc89))
- Documentation for all official extensions ([commit](https://github.com/miguelgrinberg/microdot/commit/09dc3ef7aa8e37c64f6ee919e4603c53b05bc156))
- Remove legacy `microdot-asyncio` package files ([commit](https://github.com/miguelgrinberg/microdot/commit/f1a93ec35e2e758015360b753cb9b07dbf4e96d1))
- Added MicroPython libraries required by user sessions ([commit](https://github.com/miguelgrinberg/microdot/commit/c9e148bd04aa70df2d8cc8db766eb52fa87cda31))
- Reorganized vendored MicroPython libraries ([commit](https://github.com/miguelgrinberg/microdot/commit/7df74b05374cfc398fcdeb280e93ec3f46047c2a))

**Release 0.9.0** - 2022-06-04

- Streaming responses [#44](https://github.com/miguelgrinberg/microdot/issues/44) ([commit](https://github.com/miguelgrinberg/microdot/commit/d71665fd388c92a50198faf0d761235f0138797a))
- Return 204 when view function returns None ([commit](https://github.com/miguelgrinberg/microdot/commit/71009b49781ce356155df661a66dc98170f35d63))
- ASGI support (CPython only) ([commit](https://github.com/miguelgrinberg/microdot/commit/7e8ecb199717dd90c6cb374cb0d24b54dd6ea33e))
- WSGI support (CPython only) ([commit](https://github.com/miguelgrinberg/microdot/commit/1ae51ccdf75991a2958b06f7a3439d64f92f1b69))
- Documentation updates ([commit](https://github.com/miguelgrinberg/microdot/commit/bcbad516751f1ea9928f4a6d0e8843a4334b885a))
- Add Python 3.10 to build ([commit](https://github.com/miguelgrinberg/microdot/commit/5b5eb907d83d94dde544b266e6659071e4d47ee1))
- Run linter on examples ([commit](https://github.com/miguelgrinberg/microdot/commit/c18ccccb8e0744d8670433aeeba068c5654f32df))

**Release 0.8.2** - 2022-04-20

- Remove debugging print statement [#38](https://github.com/miguelgrinberg/microdot/issues/38) ([commit](https://github.com/miguelgrinberg/microdot/commit/0f278321c8bd65c5cb67425eb837e6581cbb0054)) (thanks **Mark Blakeney**!)

**Release 0.8.1** - 2022-03-18

- Optimizations for request streams and bodies ([commit](https://github.com/miguelgrinberg/microdot/commit/29a9f6f46c737aa0fd452766c23bd83008594ac4))

**Release 0.8.0** - 2022-02-18

- Support streamed request payloads [#26](https://github.com/miguelgrinberg/microdot/issues/26) ([commit](https://github.com/miguelgrinberg/microdot/commit/992fa722c1312c0ac0ee9fbd5e23ad7b52d3caca))
- Use case insensitive comparisons for HTTP headers [#33](https://github.com/miguelgrinberg/microdot/issues/33) ([commit](https://github.com/miguelgrinberg/microdot/commit/e16fb94b2d1e88ef681d70f7f456c37ee9859df6)) (thanks **Steve Li**!)
- More robust logic to read request body [#31](https://github.com/miguelgrinberg/microdot/issues/31) ([commit](https://github.com/miguelgrinberg/microdot/commit/bd82c4deabf40d37e6b7397b08e8eb40ba2b6a42))
- Simplified `hello_async.py` example ([commit](https://github.com/miguelgrinberg/microdot/commit/c130d8f2d45dcce9606dda25d31d653ce91faf92))

**Release 0.7.2** - 2021-09-28

- Document a security risk in the send_file function ([commit](https://github.com/miguelgrinberg/microdot/commit/d29ed6aaa1f2080fcf471bf6ae0f480f95ff1716)) (thanks **Ky Tran**!)
- Validate redirect URLs ([commit](https://github.com/miguelgrinberg/microdot/commit/8e5fb92ff1ccd50972b0c1cb5a6c3bd5eb54d86b)) (thanks **Ky Tran**!)
- Return a 400 error when request object could not be created ([commit](https://github.com/miguelgrinberg/microdot/commit/06015934b834622d39f52b3e13d16bfee9dc8e5a))

**Release 0.7.1** - 2021-09-27

- Breaking change: Limit the size of each request line to 2KB. A different maximum can be set in `Request.max_readline`. ([commit](https://github.com/miguelgrinberg/microdot/commit/de9c991a9ab836d57d5c08bf4282f99f073b502a)) (thanks **Ky Tran**!)

**Release 0.7.0** - 2021-09-27

- Breaking change: Limit the size of the request body to 16KB. A different maximum can be set in `Request.max_content_length`. ([commit](https://github.com/miguelgrinberg/microdot/commit/5003a5b3d948a7cf365857b419bebf6e388593a1))
- Add documentation for `request.client_addr` [#27](https://github.com/miguelgrinberg/microdot/issues/27) ([commit](https://github.com/miguelgrinberg/microdot/commit/833fecb105ce456b95f1d2a6ea96dceca1075814)) (thanks **Mark Blakeney**!)
- Added documentation for reason argument in the Response object ([commit](https://github.com/miguelgrinberg/microdot/commit/d527bdb7c32ab918a1ecf6956cf3a9f544504354))

**Release 0.6.0** - 2021-08-11

- Better handling of content types in form and json methods [#24](https://github.com/miguelgrinberg/microdot/issues/24) ([commit](https://github.com/miguelgrinberg/microdot/commit/da32f23e35f871470a40638e7000e84b0ff6d17f))
- Accept a custom reason phrase for the HTTP response [#25](https://github.com/miguelgrinberg/microdot/issues/25) ([commit](https://github.com/miguelgrinberg/microdot/commit/bd74bcab74f283c89aadffc8f9c20d6ff0f771ce))
- Make mime type check for form submissions more robust ([commit](https://github.com/miguelgrinberg/microdot/commit/dd3fc20507715a23d0fa6fa3aae3715c8fbc0351))
- Copy client headers to avoid write back [#23](https://github.com/miguelgrinberg/microdot/issues/23) ([commit](https://github.com/miguelgrinberg/microdot/commit/0641466faa9dda0c54f78939ac05993c0812e84a)) (thanks **Mark Blakeney**!)
- Work around a bug in uasyncio's create_server() function ([commit](https://github.com/miguelgrinberg/microdot/commit/46963ba4644d7abc8dc653c99bc76222af526964))
- More unit tests ([commit](https://github.com/miguelgrinberg/microdot/commit/5cd3ace5166ec549579b0b1149ae3d7be195974a))
- Installation instructions ([commit](https://github.com/miguelgrinberg/microdot/commit/1a8db51cb3754308da6dcc227512dcdeb4ce4557))
- Run tests with pytest ([commit](https://github.com/miguelgrinberg/microdot/commit/8b4ebbd9535b3c083fb2a955284609acba07f05e))
- Deprecated the microdot-asyncio package ([commit](https://github.com/miguelgrinberg/microdot/commit/a82ed55f56e14fbcea93e8171af86ab42657fa96))

**Release 0.5.0** - 2021-06-06

- [Documentation](https://microdot.readthedocs.io/en/latest/) site ([commit](https://github.com/miguelgrinberg/microdot/commit/12cd60305b7b48ab151da52661fc5988684dbcd8))
- Support duplicate arguments in query string and form submissions [#21](https://github.com/miguelgrinberg/microdot/issues/21) ([commit](https://github.com/miguelgrinberg/microdot/commit/b0c25a1a7298189373be5df1668e0afb5532cdaf))
- Merge `microdot-asyncio` package with `microdot` ([commit](https://github.com/miguelgrinberg/microdot/commit/b7b881e3c7f1c6ede6546e498737e93928425c30))
- Added a change log ([commit](https://github.com/miguelgrinberg/microdot/commit/9955ac99a6ac20308644f02d6e6e32847d28b70c))
- Improve project structure ([commit](https://github.com/miguelgrinberg/microdot/commit/4b101d15971fa2883d187f0bab0be999ae30b583))

**Release v0.4.0** - 2021-06-04

- Add HTTP method-specific route decorators ([commit](https://github.com/miguelgrinberg/microdot/commit/a3288a63ed45f700f79b67d0b57fc4dd20e844c1))
- Server shutdown [#19](https://github.com/miguelgrinberg/microdot/issues/19) ([commit](https://github.com/miguelgrinberg/microdot/commit/0ad538df91f8b6b8a3885aa602c014ee7fe4526b))
- Update microypthon binary for tests to 1.15 ([commit](https://github.com/miguelgrinberg/microdot/commit/3bd7fe8cea4598a7dbd0efcb9c6ce57ec2b79f9c))

**Release v0.3.1** - 2021-02-06

- Support large downloads in send_file [#3](https://github.com/miguelgrinberg/microdot/issues/3) ([commit](https://github.com/miguelgrinberg/microdot/commit/3e29af57753dbb7961ff98719a4fc4f71c0b4e3e))
- Move socket import and add simple hello example [#12](https://github.com/miguelgrinberg/microdot/issues/12) ([commit](https://github.com/miguelgrinberg/microdot/commit/c5e1873523b609680ff67d7abfada72568272250)) (thanks **Damien George**!)
- Update python versions to build ([commit](https://github.com/miguelgrinberg/microdot/commit/dfbe2edd797153fc9be40bc1928d93bdee7e7be5))
- Handle Chrome preconnect [#8](https://github.com/miguelgrinberg/microdot/issues/8) ([commit](https://github.com/miguelgrinberg/microdot/commit/125af4b4a92b1d78acfa9d57ad2f507e759b6938)) (thanks **Ricardo Mendonça Ferreira**!)
- Readme update ([commit](https://github.com/miguelgrinberg/microdot/commit/1aacb3cf46bd0b634ec3bc852ff9439f3c5dd773))
- Switch to GitHub actions for builds ([commit](https://github.com/miguelgrinberg/microdot/commit/4c0afa2beca0c3b0f167fd25c6849d6937c412ba))

**Release v0.3.0** - 2019-05-05

- g, before_request and after_request ([commit](https://github.com/miguelgrinberg/microdot/commit/8aa50f171d2d04bc15c472ab1d9b3288518f7a21))
- Threaded mode ([commit](https://github.com/miguelgrinberg/microdot/commit/494800ff9ff474c38644979086057e3584573969))
- Optional asyncio support ([commit](https://github.com/miguelgrinberg/microdot/commit/3d9b5d7084d52e749553ca79206ed7060f963f9d))
- Debug mode ([commit](https://github.com/miguelgrinberg/microdot/commit/4c83cb75636572066958ef2cc0802909deafe542))
- Print exceptions ([commit](https://github.com/miguelgrinberg/microdot/commit/491202de1fce232b9629b7f1db63594fd13f84a3))
- Flake8 ([commit](https://github.com/miguelgrinberg/microdot/commit/92edc17522d7490544c7186d62a2964caf35c861))
- Unit testing framework ([commit](https://github.com/miguelgrinberg/microdot/commit/f741ed7cf83320d25ce16a1a29796af6fdfb91e9))
- More robust header checking in tests ([commit](https://github.com/miguelgrinberg/microdot/commit/03efe46a26e7074f960dd4c9a062c53d6f72bfa0))
- Response unit tests ([commit](https://github.com/miguelgrinberg/microdot/commit/cd71986a5042dcc308617a3db89476f28dd13ecf))
- Request unit tests ([commit](https://github.com/miguelgrinberg/microdot/commit/0b95feafc96dc91d7d34528ff2d8931a8aa3d612))
- More unit tests ([commit](https://github.com/miguelgrinberg/microdot/commit/76ab1fa6d72dd9deaa24aeaf4895a0c6fc883bcb))
- Async request and response unit tests ([commit](https://github.com/miguelgrinberg/microdot/commit/89f7f09b9a2d0dfccefabebbe9b83307133bd97c))
- More asyncio unit tests ([commit](https://github.com/miguelgrinberg/microdot/commit/ba986a89ff72ebbd9a65307b81ee769879961594))
- Improve code structure ([commit](https://github.com/miguelgrinberg/microdot/commit/b16466f1a9432a608eb23769907e8952fe304a9a))
- URL pattern matching unit tests ([commit](https://github.com/miguelgrinberg/microdot/commit/0a373775d54df571ceddaac090094bb62dbe6c72))
- Rename microdot_async to microdot_asyncio ([commit](https://github.com/miguelgrinberg/microdot/commit/e5525c5c485ae8901c9602da7e4582b58fb2da40))

**Release 0.2.0** - 2019-04-19

- Error handlers ([commit](https://github.com/miguelgrinberg/microdot/commit/0f2c749f6d1b9edbf124523160e10449c932ea45))
- Fleshed out example GPIO application ([commit](https://github.com/miguelgrinberg/microdot/commit/52f2d0c4918d00d1a7e46cc7fd9a909ef6d259c1))
- More robust parsing of cookie header ([commit](https://github.com/miguelgrinberg/microdot/commit/2f58c41cc89946d51646df83d4f9ae0e24e447b9))

**Release 0.1.1** - 2019-04-17

- Minor fixes for micropython ([commit](https://github.com/miguelgrinberg/microdot/commit/e4ff70cf8fe839f5b5297157bf028569188b9031))
- Initial commit ([commit](https://github.com/miguelgrinberg/microdot/commit/311a82a44430d427948866b09cb6136e60a5b1c9))
