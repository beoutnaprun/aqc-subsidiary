#### 工具使用

1、Cookie配置

前往`config.json` 配置爱企查的Cookie注意需要`url编码`


2、脚本使用

```shell
# 直接查询单位控股打印控制台 默认大于等于50控股
python3 aqc-subsidiary.py -c {单位全称}

# 查询单位子公司 自定义大于等于控股
python3 aqc-subsidiary.py -c {单位全称} -n {控股大于} 

# 查询单位子公司 自定义大于等于控股 输出子公司名到文件
python3 aqc-subsidiary.py -c {单位全称} -n {控股大于} -o {输出文件} 
```

<img width="1396" height="645" alt="image" src="https://github.com/user-attachments/assets/76c142b5-69a6-4812-9315-a273d87fb0e2" />

3、如果出现百度安全验证可自行使用代理

<img width="421" height="125" alt="image" src="https://github.com/user-attachments/assets/34ffbea1-fd90-4d26-8645-b4f89ed1ac64" />
