# Generated by Django 4.2.1 on 2025-06-06 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('busho', models.CharField(blank=True, max_length=255, null=True, verbose_name='部署')),
                ('busho_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='部署ID')),
                ('tantou', models.CharField(blank=True, max_length=255, null=True, verbose_name='担当')),
                ('tantou_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='担当ID')),
                ('last_api', models.CharField(blank=True, max_length=255, verbose_name='最終API接続')),
            ],
        ),
        migrations.CreateModel(
            name='Sfa_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mitsu_id', models.CharField(max_length=255, unique=True, verbose_name='見積ID')),
                ('mitsu_num', models.CharField(max_length=255, verbose_name='見積番号')),
                ('mitsu_ver', models.CharField(max_length=255, verbose_name='見積バージョン')),
                ('mitsu_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='見積URL')),
                ('status', models.CharField(blank=True, max_length=255, null=True, verbose_name='ステータス')),
                ('order_kubun', models.CharField(blank=True, max_length=255, null=True, verbose_name='注文区分')),
                ('nouhin_kigen', models.CharField(blank=True, max_length=255, null=True, verbose_name='納品期限日')),
                ('nouhin_shitei', models.CharField(blank=True, max_length=255, null=True, verbose_name='納品指定日')),
                ('make_day', models.CharField(blank=True, max_length=255, verbose_name='見積作成日')),
                ('update_day', models.CharField(blank=True, max_length=255, verbose_name='更新日')),
                ('juchu_day', models.CharField(blank=True, max_length=255, null=True, verbose_name='受注日')),
                ('hassou_day', models.CharField(blank=True, max_length=255, null=True, verbose_name='発送完了日')),
                ('cus_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='顧客ID')),
                ('sei', models.CharField(blank=True, max_length=255, null=True, verbose_name='姓')),
                ('mei', models.CharField(blank=True, max_length=255, null=True, verbose_name='名')),
                ('com', models.CharField(blank=True, max_length=255, null=True, verbose_name='会社名')),
                ('money', models.IntegerField(blank=True, null=True, verbose_name='金額')),
                ('busho_id', models.CharField(max_length=255, verbose_name='部署ID')),
                ('tantou_id', models.CharField(max_length=255, verbose_name='担当ID')),
                ('show', models.IntegerField(default=0, verbose_name='案件表示')),
                ('eye', models.IntegerField(default=0, verbose_name='オープン表示')),
                ('hidden_day', models.CharField(blank=True, default='', max_length=255, verbose_name='非表示日時')),
                ('s_status', models.CharField(blank=True, max_length=255, null=True, verbose_name='s_ステータス')),
            ],
        ),
    ]
