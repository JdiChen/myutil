# 1. if
格式
```sql
<if test=判断条件> sql语句 </if>
```
```sql
<select id="select"
     resultType="Blog">
  SELECT * FROM BLOG
  WHERE state = 'ACTIVE'
-- 当 title不为null时，sql增加以下条件
  <if test="title != null">
    AND title like #{title}
  </if>        
<if test="name!= null">
    AND name like #{title}
  </if>
</select>
```
# 2. where
直接可以省略sql中的 where 关键字
where会自动去除首个条件的前缀 AND 
```sql
<where>
        <if test="title != null">
            AND title like #{title}
        </if>
        <if test="name!= null">
            AND name like #{title}
        </if>
<where>
```
# 3. choose（when/otherwise）
相当于java里面的switch语句  otherwise为其它情况
```sql
<select id="findActiveBlogLike"
     resultType="Blog">
  SELECT * FROM BLOG WHERE state = 'ACTIVE'
  <choose>
--     所有when条件中选一个执行，如里都不符合，就执行otherwise中的条件
    <when test="title != null">
      AND title like #{title}
    </when>
    <when test="author != null and author.name != null">
      AND author_name like #{author.name}
    </when>
    <otherwise>
      AND featured = 1
    </otherwise>
  </choose>
</select>

```
# 4.trim
功能是填写前缀和后缀，以及忽略前后的字符
prefix：整个trim增加前缀 
suffix：整个trim增加后缀 
suffixOverrides: 首个条件忽略前导字符 
prefixOverrides：末尾条件忽略后缀字符 
```sql
    <insert id="insert" parameterType="com.example.springbootdemo.bean.TestDemo2">
        insert into test_demo
        <trim prefix="(" suffix=")" suffixOverrides=",">
            <if test="taskId != null">
                task_id,
            </if>
            <if test="wsNo != null">
                ws_no,
            </if>
        </trim>
        <trim prefix="VALUES(" suffix=")" suffixOverrides=",">
            <if test="taskId != null">
                #{taskId},
            </if>
            <if test="wsNo != null">
                #{wsNo},
            </if>
        </trim>

```
上方sql的是将下方sql拆分
```sql
insert into test_demo(task_id,ws_no) VALUES('值1','值2')
```
# 5. foreach
mybatis的foreach标签经常用于遍历集合，构建in条件语句或者批量操作语句。



参考 
```shell
https://blog.csdn.net/xjszsd/article/details/118001173
```
# 6.set
主要用于更新语句，动态设置更新字段，如果传入的字段为空则不更新 
如果所有条件都传空，则此sql会报 PSQLException 错误
```sql
<update id="dynamicSetTest" parameterType="Blog">  
    update t_blog  
    <set>  
        <if test="title != null">  
            title = #{title},  
        </if>  
        <if test="content != null">  
            content = #{content},  
        </if>  
        <if test="owner != null">  
            owner = #{owner}  
        </if>  
    </set>  
    where id = #{id}  
</update> 

```
