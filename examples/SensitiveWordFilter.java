import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Java 使用示例
 *
 * <p>演示如何加载词库并进行简单的文本过滤。
 *
 * <pre>
 * javac SensitiveWordFilter.java
 * java SensitiveWordFilter
 * </pre>
 */
public class SensitiveWordFilter {

    private final Set<String> sensitiveWords = new HashSet<>();
    private final Set<String> stopwords = new HashSet<>();

    public static Set<String> loadLineSeparated(String path) throws IOException {
        return Files.lines(Paths.get(path), StandardCharsets.UTF_8)
                .map(String::trim)
                .filter(s -> !s.isEmpty())
                .collect(Collectors.toSet());
    }

    public static Set<String> loadCommaSeparated(String path) throws IOException {
        String content = new String(Files.readAllBytes(Paths.get(path)), StandardCharsets.UTF_8);
        return Arrays.stream(content.split(","))
                .map(String::trim)
                .filter(s -> !s.isEmpty())
                .collect(Collectors.toSet());
    }

    public void loadAll(String dataDir) throws IOException {
        sensitiveWords.addAll(loadCommaSeparated(dataDir + "/色情类.txt"));
        sensitiveWords.addAll(loadCommaSeparated(dataDir + "/政治类.txt"));
        sensitiveWords.addAll(loadLineSeparated(dataDir + "/广告.txt"));
        sensitiveWords.addAll(loadLineSeparated(dataDir + "/涉枪涉爆违法信息关键词.txt"));
        stopwords.addAll(loadLineSeparated(dataDir + "/stopword.dic"));
    }

    public List<String> check(String text) {
        return sensitiveWords.stream()
                .filter(text::contains)
                .collect(Collectors.toList());
    }

    public String replace(String text, String mask) {
        String result = text;
        for (String word : sensitiveWords) {
            if (result.contains(word)) {
                result = result.replace(word, mask.repeat(word.length()));
            }
        }
        return result;
    }

    public List<String> removeStopwords(List<String> tokens) {
        return tokens.stream()
                .filter(t -> !stopwords.contains(t))
                .collect(Collectors.toList());
    }

    public static void main(String[] args) throws IOException {
        String dataDir = args.length > 0 ? args[0] : "..";

        System.out.println("加载词库...");
        long start = System.currentTimeMillis();

        SensitiveWordFilter filter = new SensitiveWordFilter();
        filter.loadAll(dataDir);

        long elapsed = System.currentTimeMillis() - start;
        System.out.printf("加载完成: %d 条敏感词, %d 条停止词 (%dms)%n%n",
                filter.sensitiveWords.size(), filter.stopwords.size(), elapsed);

        String testText = "这是一段测试文本，用于验证词库加载是否正常工作。";
        System.out.println("测试文本: " + testText);

        List<String> matches = filter.check(testText);
        if (!matches.isEmpty()) {
            System.out.println("发现敏感词: " + matches);
            System.out.println("过滤后: " + filter.replace(testText, "*"));
        } else {
            System.out.println("未发现敏感词。");
        }

        System.out.println("\n--- 停止词过滤示例 ---");
        List<String> tokens = Arrays.asList("我", "喜欢", "这个", "开源", "项目", "的", "设计");
        List<String> filtered = filter.removeStopwords(tokens);
        System.out.println("原始分词: " + tokens);
        System.out.println("去停止词: " + filtered);
    }
}
