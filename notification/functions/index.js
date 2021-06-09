const functions = require("firebase-functions");
const admin = require("firebase-admin");
admin.initializeApp();

exports.sendPushMessage = functions.firestore
  .document("Notification/{userId}")
  .onWrite(async (change, context) => {
    const data = change.after.data();
    const previousData = change.before.data();

    // uidから通知先のユーザー情報を取得
    const userRef = await admin
      .firestore()
      .collection("Users")
      .doc(context.params.userId);
    const userDoc = await userRef.get();

    if (userDoc.exists) {
      const user = userDoc.data();
      // 通知のタイトルと本文を設定
      const payload = {
        notification: {
          title: `ほげ`,
          body: data.message
        }
      };

      /// プッシュ通知を送信
      if (user.fcmToken) {
        admin.messaging().sendToDevice(user.fcmToken, payload);
      } else {
        console.error("No Firebase Cloud Messaging Token.");
      }
    } else {
      console.error("No User.");
    }

    return true;
  });