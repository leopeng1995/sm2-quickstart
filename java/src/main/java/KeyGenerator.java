import org.bouncycastle.jcajce.provider.asymmetric.ec.BCECPrivateKey;
import org.bouncycastle.jcajce.provider.asymmetric.ec.BCECPublicKey;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.math.ec.ECPoint;
import org.bouncycastle.util.encoders.Hex;

import java.math.BigInteger;
import java.security.*;
import java.security.spec.ECGenParameterSpec;

public class KeyGenerator {

    public static void main(String[] args) throws Exception {
        ECGenParameterSpec sm2Spec = new ECGenParameterSpec("sm2p256v1");
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("EC", new BouncyCastleProvider());
        kpg.initialize(sm2Spec, new SecureRandom());
        KeyPair keyPair = kpg.generateKeyPair();

        PublicKey publicKey = keyPair.getPublic();
        PrivateKey privateKey = keyPair.getPrivate();

        //-----------压缩公钥---------
        BigInteger priKeyIntD = ((BCECPrivateKey) privateKey).getD();
        ECPoint pubKeyPointQ = ((BCECPublicKey) publicKey).getQ();
        System.out.println("SM2 public key: \n"
                + "04"
                + pubKeyPointQ.getXCoord().toString()
                + pubKeyPointQ.getYCoord().toString());
        System.out.println("SM2 private key: \n"
                + Hex.toHexString(priKeyIntD.toByteArray()));
    }

}
