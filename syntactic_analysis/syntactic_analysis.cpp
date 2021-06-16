#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <stack>
#define ROW 6
#define COLUMN 7
using namespace std;

//LL(1) 分析表 R=E' Y=T'
//getTable 得到的便是下面的一张表格
string ttable[ROW][COLUMN] = {
    {"", "i", "+", "*", "(", ")", "#"},
    {"E", "TR", "", "", "TR", "", ""},
    {"R", "", "+TR", "", "", "ε", "ε"},
    {"T", "FY", "", "", "FY", "", ""},
    {"Y", "", "ε", "*FY", "", "ε", "ε"},
    {"F", "i", "", "", "(E)", "", ""}};

string table[ROW][COLUMN] = {};

void getTable(string path)
{
    int col = 0, row = 0;
    ifstream file;
    file.open(path, ios::in);
    string line;
    while (getline(file, line))
    {
        col = 0;
        stringstream sline(line);
        string str;
        while (getline(sline, str, ','))
        {
            if (str.length() > 1)
            {
                str = str.substr(2);
            }
            table[row][col++] = str;
        }
        row++;
    }
}

void printTable(string table[][COLUMN])
{
    for (int i = 0; i < ROW; i++)
    {
        for (int j = 0; j < COLUMN; j++)
        {
            cout << table[i][j] << '\t';
        }
        cout << endl;
    }
}

//从底向上输出栈
void PrintStack(stack<string> s)
{
    if (s.empty())
        return;
    string x = s.top();
    s.pop();
    PrintStack(s);
    cout << x;
    s.push(x);
}

string Get_table(string x, string a)
{
    string ans = "";
    for (int i = 0; i < ROW; i++)
    {
        for (int j = 0; j < COLUMN; j++)
        {
            if (x == table[i][0] && a == table[0][j])
            {
                ans = table[i][j];
                return ans;
            }
        }
    }
    return ans;
}

bool check_LL1(string input)
{
    bool flag = true;
    stack<string> s;
    s.push("#");
    s.push("E");
    int i = 0;
    // a 是扫描指针
    string a = input.substr(0, 1); // substr(pos,len)
    string x;
    int step = 0;
    cout << "analytical process:" << endl;
    cout << "step:\t"
         << "stack\t"
         << "input\t"
         << "input:\t"
         << "production rule" << endl;
    while (flag)
    {
        string RS;
        x = s.top(); // 上托栈顶符号放入X
        cout << ++step << "\t";
        PrintStack(s);
        cout << "\t";
        cout << a << "\t";
        cout << input.substr(i, input.length()) << "\t";
        if (x == a && a == "#")
        {
            cout << endl;
            break;
        }
        else if (x == a && a != "#") // 扫描指针的移动只发生在这一判断
        {
            s.pop();
            i++;
            a = input.substr(i, 1);
            cout << endl;
        }
        else if ((RS = Get_table(x, a)) != "")
        {
            if (RS != "ε")
            {
                cout << x << "→" << RS;
                s.pop();
                for (int j = RS.length() - 1; j >= 0; j--) // 将产生式逆序入栈
                {
                    string tmp = RS.substr(j, 1);
                    s.push(tmp);
                }
            }
            else
            {
                cout << x << "→" << RS;
                s.pop();
            }
            cout << endl;
        }
        else
        {
            flag = false;
            cout << endl;
            break;
        }
    }
    return flag;
}
int main()
{
    getTable("table.txt");
    string input;
    while (cin >> input)
    {
        input = input + "#";
        if (check_LL1(input))
        {
            cout << endl
                 << "RESULT: correct" << endl
                 << endl;
        }
        else
        {
            cout << endl
                 << "RESULT: error  " << endl
                 << endl;
        }
    }

    printTable(table);
    return 0;
}
// Reference:
// https://www.cnblogs.com/standby/p/6792814.html?utm_source=itdadao&utm_medium=referral
// https://www.cnblogs.com/standby/p/6792774.html 求FIRST集和FOLLOW集
// https://www.cnblogs.com/ISGuXing/p/11114576.html 自上而下的LL(1)语法分析法