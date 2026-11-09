package __PACKAGE__

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.view.View
import android.widget.RemoteViews
import org.json.JSONObject
import java.io.File

/** Widget "Leitura · Para ti": mostra os 4 artigos mais relevantes por ler. */
class HeadlinesWidget : AppWidgetProvider() {
    override fun onUpdate(context: Context, manager: AppWidgetManager, ids: IntArray) {
        for (id in ids) manager.updateAppWidget(id, build(context))
    }

    companion object {
        // O app (Rust) escreve widget.json na pasta de dados; procuramos onde quer que esteja.
        private fun findData(ctx: Context): File? {
            listOf(File(ctx.dataDir, "widget.json"), File(ctx.filesDir, "widget.json"))
                .firstOrNull { it.exists() }?.let { return it }
            return ctx.dataDir.walkTopDown().maxDepth(4).firstOrNull { it.name == "widget.json" }
        }

        fun build(ctx: Context): RemoteViews {
            val v = RemoteViews(ctx.packageName, R.layout.headlines_widget)
            val titles = intArrayOf(R.id.t1, R.id.t2, R.id.t3, R.id.t4)
            val sources = intArrayOf(R.id.s1, R.id.s2, R.id.s3, R.id.s4)
            var count = 0
            try {
                val f = findData(ctx)
                if (f != null) {
                    val o = JSONObject(f.readText())
                    v.setTextViewText(R.id.wtitle, o.optString("title", "Leitura"))
                    val arr = o.optJSONArray("items")
                    for (i in 0 until 4) {
                        val item = arr?.optJSONObject(i)
                        if (item != null) {
                            v.setTextViewText(titles[i], item.optString("t"))
                            v.setTextViewText(sources[i], item.optString("s"))
                            v.setViewVisibility(titles[i], View.VISIBLE)
                            v.setViewVisibility(sources[i], View.VISIBLE)
                            count++
                        } else {
                            v.setViewVisibility(titles[i], View.GONE)
                            v.setViewVisibility(sources[i], View.GONE)
                        }
                    }
                }
            } catch (e: Exception) { }
            v.setViewVisibility(R.id.wempty, if (count == 0) View.VISIBLE else View.GONE)
            val intent = ctx.packageManager.getLaunchIntentForPackage(ctx.packageName)
            if (intent != null) {
                val pi = PendingIntent.getActivity(ctx, 0, intent,
                    PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT)
                v.setOnClickPendingIntent(R.id.wroot, pi)
            }
            return v
        }

        fun refresh(ctx: Context) {
            val mgr = AppWidgetManager.getInstance(ctx)
            val ids = mgr.getAppWidgetIds(ComponentName(ctx, HeadlinesWidget::class.java))
            for (id in ids) mgr.updateAppWidget(id, build(ctx))
        }
    }
}
