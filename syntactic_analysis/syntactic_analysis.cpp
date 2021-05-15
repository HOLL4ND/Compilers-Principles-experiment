#include <iostream>
#include <string>
#include <stack>
#define ROW 6
#define COLUMN 7
using namespace std;

//LL(1) 分析表
string table[ROW][COLUMN] = {
    {"", "i", "+", "*", "(", ")", "#"},
    {"E", "Te", "", "", "Te", "", ""},
    {"e", "", "+Te", "", "", "ε", "ε"},
    {"T", "Ft", "", "", "Ft", "", ""},
    {"t", "", "ε", "*Ft", "", "ε", "ε"},
    {"F", "i", "", "", "(E)", "", ""}};

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
    while (flag)
    {
        string RS;
        x = s.top(); // 上托栈顶符号放入X
        if (x == a && a == "#")
        {
            break;
        }
        else if (x == a && a != "#") // 扫描指针的移动只发生在这一判断
        {
            s.pop();
            i++;
            a = input.substr(i, 1);
        }
        else if ((RS = Get_table(x, a)) != "")
        {
            if (RS != "ε")
            {
                s.pop();
                for (int j = RS.length() - 1; j >= 0; j--) // 将产生式逆序入栈
                {
                    string tmp = RS.substr(j, 1);
                    s.push(tmp);
                }
            }
            else
            {
                s.pop();
            }
        }
        else
        {
            flag = false;
            break;
        }
    }
    return flag;
}
int main()
{
    string input;
    while (cin >> input)
    {
        input = input + "#";
        if (check_LL1(input))
        {
            cout << "correct" << endl;
        }
        else
        {
            cout << "error" << endl;
        }
    }
    // printTable(table);
    return 0;
}
// Reference:
// https://www.cnblogs.com/standby/p/6792814.html?utm_source=itdadao&utm_medium=referral
// https://www.cnblogs.com/standby/p/6792774.html
// https://www.cnblogs.com/ISGuXing/p/11114576.html