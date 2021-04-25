# диаграмма классов проекта
# sudo apt install graphviz

# тестирование
#apt install siege
#siege -f /home/django/geekshop/urls_siege.txt -d1 -r10 -c1
#siege -f /home/django/geekshop/urls_siege.txt -d1 -r10 -c5


# тестирование со входом в учетную запись
#siege -f /home/django/geekshop/urls_siege_login.txt -d1 -r10 -c1 --debug

# homework_2_6
siege -f /home/django/geekshop/urls_siege_login.txt -d1 -r10 -c10g