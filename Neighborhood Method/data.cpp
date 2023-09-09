#include <iostream>
#include <cstdio>
 using namespace std;
 int main()
 {
 	freopen ("trainset.txt","r",stdin);
 	freopen ("train_recqdata.csv","w",stdout);
 	double a;
	int n = 0;
 	/*while (cin>>a){
 		n++;
 		if (n%3==0){
 			cout<<"\n";
 			continue;
 		}
 		cout<<a;
 		if (n%4!=3)
 		    cout<<",";
    }*/
    while (cin>>a){
    	cout<<a;
    	n++;
    	if (n%3 == 0)
    		cout<<"\n";
    	else
    	    cout<<",";
    	}
 	
 	return 0;
 }
