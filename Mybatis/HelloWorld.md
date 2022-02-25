#1.下载依赖
mybatis和对应的数据库驱动
```xml
    <dependencies>
        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis</artifactId>
            <version>3.5.9</version>
        </dependency>
        
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <version>42.3.3</version>
        </dependency>
    </dependencies>
```
#2.创建数据库表的实体类
testdemo表内有username和age字段,实体类如下
```java
public class TestDemo {
    //在没有使用另名的情况下，这里需要和数据库字段名称一致
    private String username;
    private int age;

    @Override
    public String toString() {
        return "TestDemo{" +
                "username='" + username + '\'' +
                ", age='" + age + '\'' +
                '}';
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getAge() {
        return age;
    }

    public void setAge(String age) {
        this.age = age;
    }
}

```
#3创建mapper.xml映射文件
每个xml文件都有对应的namespace  
即mybatis是通过名称空间来查找对应的java类或者接口
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.cq.mybatis.maaper">
    <select id="select" resultType="com.cq.mybatis.module.TestDemo">
        select * from test_demo
    </select>
</mapper>
```
#4.创建mybatis配置文件
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
<!--    环境信息-->
<!--    配置选择哪个环境,配置多个后可选择是生产环境还是测试环境-->
    <environments default="dev">
<!--        可以配置多个environment-->
        <environment id="dev">
            <transactionManager type="JDBC"/>            
            <dataSource type="POOLED">
                <property name="driver" value="sql driver"/>
                <property name="url" value="you url"/>
                <property name="username" value="username"/>
                <property name="password" value="password"/>
            </dataSource>
        </environment>
    </environments>
<!--    查找的mapper-->
    <mappers>
<!--        这里输入资源路径,不是包-->
        <mapper resource="usermapper.xml"/>        
    </mappers>
</configuration>
```
运行时找不到包的处理方法  
默认情况下,只会去查找resources文件下的配置文件,且不会编译进去  
在maven配置文件中增加如下配置  
```xml
    <build>
        <resources>
            <resource>
                <directory>/src/main/java</directory>
                <includes>
                    <include>**/*.xml</include>
                </includes>
            </resource>
            <resource>
                <directory>/src/main/resources</directory>
            </resource>
        </resources>
    </build>
```
#5调用方式
使用TestNg新建测试类的方式，也可以直接写一个main方法
```java
public class test {
    SqlSession sqlSession;
    @BeforeTest
    public void setup() throws IOException {
        //读取mybatis配置文件
        SqlSessionFactory factory = new SqlSessionFactoryBuilder().build(Resources.getResourceAsStream("mybatisConfig.xml"));
        sqlSession = factory.openSession();

    }
    @Test
    public void testSelect(){
        //读取对应的sql
        // selectList的参数是mapper.xml中 namespace.id 的方式
        List<TestDemo> demos = sqlSession.selectList("com.cq.mybatis.maaper.TestDemo.select");
        for (TestDemo demo:
                demos) {
            System.out.println(demo);
        }

    }
    @AfterTest
    public void teardown(){
        sqlSession.close();
    }
}
```
#第二种方法
实体类不用变，需要创建对应的配置文件映射接口，再创建对应的配置文件
## 1.创建映射接口
```java
public interface UserMapper {
    //注意是，这里的方法名和xml文件中的id一致，否则会找不到调用
    List<TestDemo> getDemos();
}
```
## 2.创建xml文件
注意  
1. xml的文件名，需要和映射接口的接口名一致，否则会找不到映射  
2. xml中的namespace需要是完整的接口名
3. sql语句的id需要和接口方法名称一致
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.cq.mybatis.maaper.UserMapper">
<!--    这里的id需要和映射接口中的方法名一致-->
    <select id="getDemos" resultType="com.cq.mybatis.module.TestDemo">
        select * from test_demo
    </select>
</mapper>
```
## 3.配置查找路径
在mybatis配置文件中，修改mapper的查找方式如下  
即接口文件和配置文件所在的包下
```xml
    <mappers>
        <package name="com.cq.mybatis.maaper"/>
    </mappers>
```
## 4.调用方式
在方法一的基础上，增加一个读取mapper的语句
```java
public class test {
    SqlSession sqlSession;
    UserMapper mapper;
    @BeforeTest
    public void setup() throws IOException {
        SqlSessionFactory factory = new SqlSessionFactoryBuilder().build(Resources.getResourceAsStream("mybatisConfig.xml"));
        sqlSession = factory.openSession();
        // 读取接口给变量，然后由mybatis去查找对应sql语句
        mapper = sqlSession.getMapper(UserMapper.class);
    }
    @Test
    public void testSelect(){
//        List<TestDemo> demos = sqlSession.selectList("com.cq.mybatis.maaper.TestDemo.select");
        List<TestDemo> demos = mapper.getDemos();
        for (TestDemo demo:
             demos) {
            System.out.println(demo);
        }
    }
    @AfterTest
    public void teardown(){
        sqlSession.close();
    }
}
```
# 步骤总结
1. 创建数据库
2. 创建数据库实体类
3. 创建映射接口
4. 根据映射接口创建映射xml文件（namespace=接口全名）
5. 创建mybatis配置文件（mapper选择包扫瞄）
6. 使用 SqlSessionFactoryBuilder 得到factory对象
7. factoty.openSession()得到操作对象
8. 操作对象使用getMapper(接口.class)得到实例
9. 实例直接调用方法即可实现数据库调用
