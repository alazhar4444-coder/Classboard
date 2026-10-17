package om.maadh.school;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Base64;
import androidx.core.content.FileProvider;
import java.io.File;
import java.io.FileOutputStream;
import android.print.PrintAttributes;
import android.print.PrintDocumentAdapter;
import android.print.PrintManager;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private WebView web;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        web = new WebView(this);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        web.addJavascriptInterface(new Bridge(), "Android");
        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) {
                return openExternal(r.getUrl());
            }
            @Override
            public boolean shouldOverrideUrlLoading(WebView v, String url) {
                return openExternal(Uri.parse(url));
            }
        });
        web.getSettings().setSupportMultipleWindows(false);
        setContentView(web);
        if (savedInstanceState != null) web.restoreState(savedInstanceState);
        else web.loadUrl("file:///android_asset/index.html");
    }

    private boolean openExternal(Uri uri) {
        String sc = uri.getScheme();
        if ("file".equals(sc)) return false;
        try { startActivity(new Intent(Intent.ACTION_VIEW, uri)); } catch (Exception ignored) {}
        return true;
    }

    @Override protected void onSaveInstanceState(Bundle out) { super.onSaveInstanceState(out); web.saveState(out); }

    @Override public void onBackPressed() { if (web.canGoBack()) web.goBack(); else super.onBackPressed(); }

    class Bridge {
        @JavascriptInterface public void share(String text) {
            Intent i = new Intent(Intent.ACTION_SEND);
            i.setType("text/plain");
            i.putExtra(Intent.EXTRA_TEXT, text);
            startActivity(Intent.createChooser(i, "مشاركة"));
        }
        @JavascriptInterface public void shareImage(String b64) {
            try {
                File dir = new File(getCacheDir(), "shared");
                dir.mkdirs();
                File f = new File(dir, "ehtiyat.png");
                FileOutputStream out = new FileOutputStream(f);
                out.write(Base64.decode(b64, Base64.DEFAULT));
                out.close();
                Uri uri = FileProvider.getUriForFile(MainActivity.this, "om.maadh.school.files", f);
                Intent i = new Intent(Intent.ACTION_SEND);
                i.setType("image/png");
                i.putExtra(Intent.EXTRA_STREAM, uri);
                i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                String[] pkgs = {"com.whatsapp", "com.whatsapp.w4b"};
                for (String pkg : pkgs) {
                    try { i.setPackage(pkg); startActivity(i); return; } catch (Exception ignored) {}
                }
                i.setPackage(null);
                startActivity(Intent.createChooser(i, "إرسال جدول الاحتياط"));
            } catch (Exception e) { e.printStackTrace(); }
        }
        @JavascriptInterface public void whatsapp(String text) {
            String[] pkgs = {"com.whatsapp", "com.whatsapp.w4b"};
            for (String pkg : pkgs) {
                try {
                    Intent i = new Intent(Intent.ACTION_SEND);
                    i.setType("text/plain");
                    i.setPackage(pkg);
                    i.putExtra(Intent.EXTRA_TEXT, text);
                    startActivity(i);
                    return;
                } catch (Exception ignored) {}
            }
            share(text);
        }
        @JavascriptInterface public void copy(String text) {
            ClipboardManager cm = (ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
            cm.setPrimaryClip(ClipData.newPlainText("maadh", text));
        }
        @JavascriptInterface public void print() {
            runOnUiThread(() -> {
                PrintManager pm = (PrintManager) getSystemService(PRINT_SERVICE);
                PrintDocumentAdapter a = web.createPrintDocumentAdapter("مدرسة معاذ");
                pm.print("مدرسة معاذ", a, new PrintAttributes.Builder().build());
            });
        }
    }
}
