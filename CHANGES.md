# Microdot change log

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
