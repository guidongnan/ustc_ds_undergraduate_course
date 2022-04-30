/*
��������������⣺
	1. ���ö�̬�滮�������
	2. ����������˿��ӻ����
	3. �������m[i,j]��s[i,j]
*/
#define MAX 9223372036854775807
#include<vector>
#include<cstdio>
#include<fstream> 
#include<iostream> 
#include <iomanip>
#include<ctime>
#include<string>
#include<windows.h>
#include<sstream>
using namespace std;


void print_s(vector< vector<int> > s, int i,int j,string &str)
{
	if(i==j)
	{
		stringstream ss;
		ss<<i;
		
		str += "A" + string(ss.str());
	}
	else
	{
		str += "(" ;
		print_s(s,i,s[i][j],str);
		print_s(s,s[i][j]+1,j,str);
		str += ")" ;
	}
	
}

void matrix_chain_order(vector<long long> &p,vector< vector<long long> > &m,vector< vector<int> > &s,double &time)
{
    LARGE_INTEGER nFreq;
	LARGE_INTEGER nBeginTime;
	LARGE_INTEGER nEndTime;
	QueryPerformanceFrequency(&nFreq);
    QueryPerformanceCounter(&nBeginTime);//��ʼ��ʱ
    
    
    
    int n =p.size();
	n =n-1;
	for(int i=1;i<n;i++)
	{
		m[i][i]=0;
	}
	for(int l=2;l<=n;l++)
	{
		for(int i=1;i<=n-l+1;i++)
		{
			int j=i+l-1;
			m[i][j]=MAX;
			for(int k=i;k<=j-1;k++)
			{
				long long q=m[i][k]+m[k+1][j]+p[i-1]*p[k]*p[j];
				if(q<m[i][j])
				{
					m[i][j]=q;
					s[i][j]=k;
				}
			}
		}
	}
    
    
    QueryPerformanceCounter(&nEndTime);//ֹͣ��ʱ
	
	time=(double)(nEndTime.QuadPart-nBeginTime.QuadPart)/(double)nFreq.QuadPart;
	
	/*
	��ӡ��� 
	*/
	
////	cout<< "m[i,j]����Ϊ��"<<endl;
////	for(int i=1;i<m.size();i++)
////	{
////		cout << setfill(' ') << setw(20) << i ; 
////	 } 
////	cout<< endl;
////	for(int i=1;i<m.size();i++)
////	{
////		for (int j=1;j<m[i].size();j++)
////		{
////			cout << setfill(' ') << setw(20) << m[i][j];
////		}
////		cout << "\t" << i << endl;
////		
////	 }
//	 
//	 
////	cout<< "s[i,j]����Ϊ��"<<endl;
////	for(int i=1;i<s.size();i++)
////	{
////		cout << setfill(' ') << setw(5) << i ; 
////	 } 
////	cout<< endl;
////	for(int i=1;i<s.size();i++)
////	{
////		for (int j=1;j<s[i].size();j++)
////		{
////			cout << setfill(' ') << setw(5) << s[i][j];
////		}
////		cout << "\t" << i << endl;
////		
////	 }
////	print_s(s,1,s.size()-1);
	cout << endl;
}






int main()
{
	
	ifstream infile("../input/1_1_input.txt");
	if (!infile.is_open())
	{
		cout << "can not open this file" << endl;
		return 0;
	}
	
	/*
	��ȡ�ļ� 
	*/
	vector< vector<long long> >list;
	for(int j=0;j<5;j++)           // ��δ���ļ�����һֱѭ��
    {
    	
		int n;
        infile >> n;
//        cout << "��С" << n << endl;
		long long long_temp;
		vector<long long> vector_temp;
		for(int i=0;i<n+1;i++)
		{
			infile >> long_temp;
			vector_temp.push_back(long_temp);
//			cout << long_temp <<endl;
		}
		list.push_back(vector_temp);
        
    }
    
    infile.close();
    
    
    /*
	����ÿ������ 
	*/
    for(int i=0;i<5;i++)
    {
    	vector<long long> p=list[i];
    	int n = p.size();
    	
    	vector< vector<long long> > m(n);//ָ������
		for(int j=0; j<m.size(); j++)
			m[j].resize(n);			//ָ������
			
    	vector< vector<int> > s(n);//ָ������
		for(int j=0; j<s.size(); j++)
			s[j].resize(n);			//ָ������
		
		double time;
		cout << "��" << i+1 << "��,����" << n-1 << "������,������˷���Ϊ��" <<endl; 
		matrix_chain_order(p,m,s,time);
		
		
		/*
		д���ļ� 
		*/
		
		string str;
		print_s(s,1,s.size()-1,str);
		cout<<str<<endl;
		
		fstream outfile;
		outfile.open("../output/result.txt",ios::out|ios::app);
		outfile << m[1][m.size()-1] << endl;
		
		outfile << str << endl;
		outfile.close();
		
		fstream outfile2;
		outfile2.open("../output/time.txt",ios::out|ios::app);
		outfile2 << time << endl;
		outfile2.close();
		
		
	}
    
    
}
