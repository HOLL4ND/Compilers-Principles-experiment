import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class LLone {
    public static ArrayList<String> production = new ArrayList<String>();
    public static String startStrSeq = "";// 非终结符，开始符在array中的顺序
    public static String startStr = "";// 非终结符集合
    public static int numNotEnd = 0;
    public static HashMap<String, String> firstMap = new HashMap<String, String>();
    public static HashMap<String, String> followMap = new HashMap<String, String>();
    public static HashMap<String, Integer> followMapCount = new HashMap<String, Integer>();
    public static HashMap<String, Integer> followMapLastCount = new HashMap<String, Integer>();

    public static void getproduction(File productTxt) throws IOException {
        try (BufferedReader br = new BufferedReader(new FileReader(productTxt))) {
            String line = null;
            while ((line = br.readLine()) != null) {
                if (line.indexOf("|") == -1) {
                    production.add(line);
                    firstMap.put(line.substring(0, 1), "");
                    followMap.put(line.substring(0, 1), "");
                    followMapCount.put(line.substring(0, 1), 0);
                    followMapLastCount.put(line.substring(0, 1), 0);
                    startStrSeq = startStrSeq + line.substring(0, 1);
                } else {
                    Stack<Integer> position = new Stack<Integer>();
                    Integer pos = line.indexOf("|");
                    while (pos != -1) {
                        position.push(pos);
                        pos = line.indexOf("|", pos + 1);
                    }
                    while (!position.empty()) {
                        int index = position.pop();
                        String rightToken = line.substring(index + 1);
                        line = line.substring(0, index);
                        String leftPro = line.substring(0, 2);
                        String newPro = leftPro + rightToken;
                        production.add(newPro);
                        startStrSeq = startStrSeq + newPro.substring(0, 1);

                    }
                    production.add(line);
                    firstMap.put(line.substring(0, 1), "");
                    followMap.put(line.substring(0, 1), "");
                    followMapCount.put(line.substring(0, 1), 0);
                    followMapLastCount.put(line.substring(0, 1), 0);
                    startStrSeq = startStrSeq + line.substring(0, 1);
                }
            }
        }
    }

    public static void printProduction() {
        for (String str : production)
            System.out.println(str);
    }

    public static void findFirst(String s, String c) {
        if (c.charAt(0) < 65 || c.charAt(0) > 90) {
            String nowHaveFirst = firstMap.get(s);
            if (nowHaveFirst.indexOf(c) == -1) {
                nowHaveFirst = nowHaveFirst + c;
                firstMap.put(s, nowHaveFirst);
            }
        } else {
            int startPoint = 0;
            startPoint = startStrSeq.indexOf(c);
            int endPoint = startStrSeq.lastIndexOf(c);
            for (; startPoint <= endPoint; startPoint++) {
                String nextProduct = production.get(startPoint);
                findFirst(s, nextProduct.substring(2, 3));
            }
        }

    }

    public static void oneFindFollow(String notEnd) {
        int endIndex;
        int addedLength = 0;
        for (String product : production) {
            endIndex = product.indexOf(notEnd);
            if (endIndex == 0 || endIndex == -1) {
                continue;
            }
            if (endIndex != product.length() - 1) {
                // 找到该字符follow的字符b
                String EndRightb = product.substring(endIndex + 1, endIndex + 1 + 1);
                String addedFollow = "";
                // 终结符直接加入follow
                if (EndRightb.charAt(0) < 65 || EndRightb.charAt(0) > 90) {
                    String thisEndFollow = followMap.get(notEnd);
                    addedFollow = (thisEndFollow + EndRightb).replaceAll("(?s)(.)(?=.*\\1)", "");
                    followMap.put(notEnd, addedFollow);
                    addedLength = addedFollow.length();
                } else {
                    // 找到该字符的first集
                    String firstOfEndRightb = firstMap.get(EndRightb);
                    if (firstOfEndRightb.indexOf("ε") != -1) {
                        addedFollow = followMap.get(product.substring(0, 1));
                    }
                    // 去除 ε
                    firstOfEndRightb = firstOfEndRightb.replace("ε", "");
                    String thisEndFollow = followMap.get(notEnd);
                    addedFollow = (addedFollow + thisEndFollow + firstOfEndRightb).replaceAll("(?s)(.)(?=.*\\1)", "");
                    followMap.put(notEnd, addedFollow);
                    addedLength = addedFollow.length();
                }
            } else if (endIndex == product.length() - 1) {
                String thisEndFollow = followMap.get(notEnd);
                String followOfLeft = followMap.get(product.substring(0, 1));
                String addedFollow = (thisEndFollow + followOfLeft).replaceAll("(?s)(.)(?=.*\\1)", "");
                followMap.put(notEnd, addedFollow);
                addedLength = addedFollow.length();
            }
            followMapCount.put(notEnd, addedLength);
        }

    }

    public static Boolean checkIsFinished() {
        Boolean isFinished = true;
        for (String str : followMapCount.keySet()) {
            if (followMapCount.get(str) > followMapLastCount.get(str)) {
                isFinished = false;
            }
            followMapLastCount.put(str, followMapCount.get(str));
        }
        return isFinished;
    }

    public static void findfollow(String allNotEnd) {
        Boolean isFinshed = false;
        for (String s : followMap.keySet()) {
            followMap.put(s, "#");
        }
        while (!isFinshed) {
            for (int i = 0; i < allNotEnd.length(); i++) {
                String notEnd = allNotEnd.substring(i, i + 1);
                oneFindFollow(notEnd);
            }
            isFinshed = checkIsFinished();
        }
    }

    public static void findfollowTest(String testing) {
        // 测试单个follow集的查找
        followMap.put("E", "#)");
        followMap.put("R", "#)");
        followMap.put("T", "#)+");
        followMap.put("F", "*+#)");
        followMap.put("Y", "#)+");
        followMap.remove(testing);
        oneFindFollow(testing);
    }

    public static void doProcessing() throws Exception {
        File proTxt = new File("pro.txt");
        getproduction(proTxt);
        for (String str : production) {
            findFirst(str.substring(0, 1), str.substring(2, 3));
        }
        startStr = startStrSeq.replaceAll("(?s)(.)(?=.*\\1)", "");
        numNotEnd = startStr.length();
        findfollow(startStr);
    }

    public static void print_llOne_Table(String[][] table, int row, int col) throws Exception {
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                String str = table[i][j];
                if (str == null) {
                    System.out.print("\t");
                    continue;
                }
                if (str != null && str.equals(new String("R"))) {
                    System.out.print("E'\t");
                } else if (str != null && str.equals(new String("Y"))) {
                    System.out.print("T'\t");
                } else {
                    System.out.print(table[i][j] + "\t");
                }
            }
            System.out.println("");
        }
    }

    public static void tableCreate() throws Exception {
        String endStr = "i+*()#";
        String[][] ll1_table = new String[numNotEnd + 1][endStr.length() + 1];
        for (int i = 1; i < endStr.length() + 1; i++) {
            ll1_table[0][i] = endStr.substring(i - 1, i);
        }
        for (int j = 1; j < numNotEnd + 1; j++) {
            ll1_table[j][0] = startStr.substring(j - 1, j);
        }
        // 对于每个非终结符
        for (String notEnd : firstMap.keySet()) {
            String thisFirst = firstMap.get(notEnd);
            if (thisFirst.indexOf("ε") != -1) {
                thisFirst = thisFirst.replace("ε", "");
                String thisFollow = followMap.get(notEnd);
                for (int i = 0; i < thisFollow.length(); i++) {
                    String singleStr = thisFollow.substring(i, i + 1);
                    int colIndex = endStr.indexOf(singleStr) + 1;
                    int rowIndex = startStr.indexOf(notEnd) + 1;
                    String tableContent = notEnd + "->ε";
                    tableContent = tableContent.replace("R", "E'");
                    tableContent = tableContent.replace("Y", "T'");
                    ll1_table[rowIndex][colIndex] = tableContent;
                }
            }
            for (int j = 0; j < thisFirst.length(); j++) {
                String singleStr = thisFirst.substring(j, j + 1);
                int colIndex = endStr.indexOf(singleStr) + 1;
                int rowIndex = startStr.indexOf(notEnd) + 1;
                String tableContent = getNotNullProduction(notEnd, singleStr);
                if (tableContent.length() != 0) {
                    tableContent = tableContent.replace("R", "E'");
                    tableContent = tableContent.replace("Y", "T'");
                    ll1_table[rowIndex][colIndex] = tableContent;
                }
            }
        }

        print_llOne_Table(ll1_table, numNotEnd + 1, endStr.length() + 1);

    }

    public static String getNotNullProduction(String notEnd, String firstStr) {
        String pro = "";
        int startIndex = startStrSeq.indexOf(notEnd);
        int endIndex = startStrSeq.lastIndexOf(notEnd);
        for (; startIndex <= endIndex; startIndex++) {
            pro = production.get(startIndex);
            if (pro.indexOf("ε") == -1) {
                if (pro.indexOf(firstStr) == 2) {
                    return pro;
                }
            }
        }
        return pro;
    }

    public static void main(String[] args) throws Exception {
        doProcessing();
        System.out.println("First set:");
        System.out.println(firstMap);
        System.out.println("");
        System.out.println("Follow set:");
        System.out.println(followMap);
        System.out.println("");
        tableCreate();
    }
}
