注：这是一篇简单记录国密算法示例的笔记，不涉及具体算法原理的描述，如有需要可参考国家密码局公布的算法描述手册。

鸣谢：greendow 公开的仓库 [SM2-signature-creation-and-verification](https://github.com/greendow/SM2-signature-creation-and-verification)，本笔记所依赖的 OpenSSL 部分是参考于此。

国密算法是一组算法，SM 代表的是国产商用密码。这里我重点只说 SM2 和 SM3，大致区分如下：

* SM2：椭圆曲线公钥密码算法。对应 ECC 椭圆曲线密码，SM2 推荐了一条256位的曲线作为标准曲线。（注：OpenSSL 我目前感觉它也就只支持了 256 位的曲线）
* SM3：杂凑算法。开始我并不能理解什么叫“杂凑”，名字感觉怪怪的，简单来说就是对消息进行哈希、散列：「此算法对输入长度小于2的64次方的比特消息，经过填充和迭代压缩，生成长度为256比特的杂凑值，其中使用了异或，模，模加，移位，与，或，非运算，由填充，迭代过程，消息扩展和压缩函数所构成。具体算法及运算示例见SM3标准。」（摘自 https://m.qukuaiwang.com.cn/news/2271.html）

#### SM3withSM2

简答来说就是：SM2.sign(SM3(Z+MSG)，PrivateKey)。

注：这里要指出，RSA 和 SM2 的公私钥格式是不同的。

#### Java 示例

使用 bouncycastle 库。主要就是三部分，生成 SM2 密钥、加签和验签：

* 生成密钥：[https://github.com/leopeng1995/sm2-quickstart/blob/master/java/src/main/java/KeyGenerator.java](https://github.com/leopeng1995/sm2-quickstart/blob/master/java/src/main/java/KeyGenerator.java)
* 加签：[https://github.com/leopeng1995/sm2-quickstart/blob/master/java/src/main/java/Signer.java](https://github.com/leopeng1995/sm2-quickstart/blob/master/java/src/main/java/Signer.java)
* 验签：[https://github.com/leopeng1995/sm2-quickstart/blob/master/java/src/main/java/Verifier.java](https://github.com/leopeng1995/sm2-quickstart/blob/master/java/src/main/java/Verifier.java)

#### Python 示例

* 验签：[https://github.com/leopeng1995/sm2-quickstart/blob/master/python/verify.py](https://github.com/leopeng1995/sm2-quickstart/blob/master/python/verify.py)
* 加签：[https://github.com/leopeng1995/sm2-quickstart/blob/master/python/sign_and_verify.py](https://github.com/leopeng1995/sm2-quickstart/blob/master/python/sign_and_verify.py)

Python 示例实际上是通过 ctypes FFI 来调用 OpenSSL C 库，因此需要执行 `build_lib.sh` 编译动态链接库。我主要是基于原仓库增加了 `sm2_api.h` 和 `sm2_api.c` 两个文件，主要是提供一个更简单的 SM2 接口，在 C 中进行 HEX 编解码：

```c
int sm2_verify(const unsigned char *message,
               const int message_len,
               const unsigned char *id,
               const int id_len,
               const unsigned char *pub_key,
               const unsigned char *r,
               const unsigned char *s);

// 返回 signature，是 r 和 s 的拼接，64 个字节。
char* sm2_sign(const unsigned char *message,
               const int message_len,
               const unsigned char *id,
               const int id_len,
               const unsigned char *pub_key,
               const unsigned char *pri_key);

// 释放 malloc 创建的内存空间。
void sm2_free(char *sig);
```
