# 1.IOC概念
Inversion of Control,控制反转  
即将对象的控制权交由spring,由spring代替人工去操作对象,省去了操作对象的代码  
操作包括创建,初始化,销毁等  
主要用到以下名词  
bean:spring中一个bean代表一个对象,对象的其它属性设置都基于bean  
context:上下文管理窗口,用于从Spring获取对象
# 2.配置方式
配置方式有三种
1. XML方式
2. JAVA代码方式
3. 混合方式,即JAVA代码中读取XML配置方式  

主要依赖spring-context包
```
<dependency>
	<groupId>org.springframework</groupId>
	<artifactId>spring-context</artifactId>
	<version>5.2.9.RELEASE</version>
</dependency>
```
# 3.xml方式
## 3.1 创建Spring.xml配置文件
下载完依赖后,IDEL会出现对象的选项,右击目录会有SpringConfig选项,输入任意文件名,即可创建Sring配置文件
## 3.2 读取文件方式
主类中使用 ClassPathXmlApplicationContext() 方法调用
```
package SpringIocDemo;
import org.springframework.context.support.ClassPathXmlApplicationContext;
public class Main {
    public static void main(String[] args) {
        //xml 配置方式
        ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("spring.xml");
        User user = context.getBean("getUser", User.class);
        System.out.println(user);
    }
```
## 3.3 注入
IOC对象及其属性注入首先需要有这个对象,项目内创建一个User对象,且这个对象的所有属性需要有getter和setter方法,否则注入不会生效
```
package SpringIocDemo;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Properties;

public class User {
    private String name;
    private int age;
    private String sex;
    private Cat cat;
    private Cat[] cats;
    private List<String> favoryter;
    private Map<String,Object> mymap;
    private Properties myper;

    public Properties getMyper() {
        return myper;
    }

    @Override
    public String toString() {
        return "User{" +
                "name='" + name + '\'' +
                ", age=" + age +
                ", sex='" + sex + '\'' +
                ", cat=" + cat +
                ", cats=" + Arrays.toString(cats) +
                ", favoryter=" + favoryter +
                ", mymap=" + mymap +
                ", myper=" + myper +
                '}';
    }

    public void setMyper(Properties myper) {
        this.myper = myper;
    }

    public Map<String, Object> getMymap() {
        return mymap;
    }

    public void setMymap(Map<String, Object> mymap) {
        this.mymap = mymap;
    }

    public List<String> getFavoryter() {
        return favoryter;
    }

    public void setFavoryter(List<String> favoryter) {
        this.favoryter = favoryter;
    }

    public Cat[] getCats() {
        return cats;
    }

    public void setCats(Cat[] cats) {
        this.cats = cats;
    }

    public Cat getCat() {
        return cat;
    }

    public void setCat(Cat cat) {
        this.cat = cat;
    }

    public User(){
        System.out.println("init");
    }

    public User(String name, int age, String sex) {
        this.name = name;
        this.age = age;
        this.sex = sex;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getSex() {
        return sex;
    }

    public void setSex(String sex) {
        this.sex = sex;
    }
}

```
以下均在xml文件内操作
### 3.3.1 Bean的获取
`<bean id="用于查找的唯一id" class="类的路径"/>`
如  
`<bean id="userid" class="SpringIocDemo.User">`  
id最好使用与类名相同,便于记忆  
这样在主类中使用如下代码即可读取到spring创建的User对象
```java
ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("spring.xml");
User user = context.getBean("getUser", User.class);
System.out.println(user);
```
### 3.3.2 构造方法注入
使用 constructor-arg 参数  
需要有对应的有参构造方法  
name的值为对应的属性名,value为需要注入的值
```xml
    <bean id="user1" class="SpringIocDemo.User">
        <constructor-arg name="name" value="test"/>
        <constructor-arg name="age" value="12"/>
        <constructor-arg name="sex" value="famale"/>
    </bean>
```
### 3.3.3 property参数注入属性
```xml
    <bean id="user2" class="SpringIocDemo.User">
        <property name="sex" value="male"/>
        <property name="name" value="user2"/>
    </bean>
```
### 3.3.4 P名称空间注入属性
P名称空间需要手动引入
`xmlns:p="http://www.springframework.org/schema/p`  
P后面直接是 属性名:属性值  
`<bean id="user3" class="SpringIocDemo.User" p:name="user3"/>`
### 3.3.5 工厂方法注入对象
第一行为静态工厂方法  
第二,三行为实例工厂方法
```xml
<bean class="SpringIocDemo.MyFactory" id="factory" factory-method="getinstance"/>
<bean class="SpringIocDemo.MyFactory" id="factory2" />
<bean class="SpringIocDemo.MyFactory" factory-bean="factory2" factory-method="getinstance2" id="factory3"/>
```
静态工厂方法  
需要新建工厂类,并且在工厂类中编写工厂方法,返回需要的实例    
再使用 factory-method 参数传入工厂方法,再主类中获取这个bean即可  
实例工厂方法则有一些不同,需要先定义工厂类的bean  
再通过 factory-bean 获取到工厂类的实例,最通过 factory-method 传入工厂方法
### 3.3.6 对象属性注入
使用 ref 属性指向对应的baen
```xml
    <bean class="SpringIocDemo.User" id="user">
        <property name="cat" ref="cat"/>
    </bean>
    <bean class="SpringIocDemo.Cat" id="cat">
        <property name="name" value="this cat"/>
        <property name="age" value="20"/>
    </bean>
```
### 3.3.7 复杂属性注入
array 注入列表  
list 注入数组  
map 注入 map  
props 注入 properties
```xml
    <bean class="SpringIocDemo.User" id="user5">
        <property name="cats">
            <array>
                <ref bean="cat"/>
                <bean class="SpringIocDemo.Cat" id="cat2">
                    <property name="name"  value="cat2name"/>
                    <property name="age"    value="12"/>
                </bean>
            </array>
        </property>
    </bean>

    <bean class="SpringIocDemo.User" id="user4">
        <property name="favoryter">
            <list>
                <value>u1</value>
                <value>u2</value>
                <value>u3</value>
                <value>u4</value>
            </list>
        </property>
    </bean>

    <bean class="SpringIocDemo.User" id="user6">
        <property name="mymap">
            <map>
                <entry key="m2" value="m2val"/>
                <entry key="m1" value-ref="cat"/>
            </map>
        </property>
    </bean>

    <bean class="SpringIocDemo.User" id="user7">
        <property name="myper">
            <props>
                <prop key="p1">p1val</prop>
                <prop key="p2">p2val</prop>
            </props>
        </property>
    </bean>
```
# 4. Java配置类方式
步骤
1. 创建JavaConfig类名随意  
2. 使用 @Configuration 注解此类,使其成为配置类
3. 创建获取实例的方法,并使用 @Bean 注解,使其成为Bean,供context调用
4. 主类中使用 AnnotationConfigApplicationContext(JavaConfig.class) 获取配置类上下文  
各种属性的注入同Java编码,无需要特殊配置
```java
package SpringIocDemo;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class JavaConfig {
    @Bean
    public User getUser(){
        User u = new User();
        u.setAge(12);
        u.setName("javaconfig");
        u.setCat(getCat());
        u.setCats(new Cat[]{getCat(),getCat()});
        return u;
    }

    @Bean
    public Cat getCat(){
        Cat cat = new Cat();
        cat.setAge(1);
        cat.setName("catname");
        return cat;
    }
}

```
主类调用
```java
        AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(JavaConfig.class);
        User user = context.getBean("getUser", User.class);
        System.out.println(user);

```
# 5.自动注入
自动注入主要依赖以下四个注解,都是基于Component编写,目前功能一致  
1. @Component,用于其它组件
2. @Respository,用于Dao层
3. @Service,用于Service层
4. @Controllar,用于Controller层

步骤
1. 创建配置类或者配置文件
2. 在目标对象上使用 @Autowired @Resources @Injected注解
3. 在配置类或者配置文件中配置自动扫瞄的路径   

注意点:  
Autowired是根据类型去查找,只能有一个对象,否则会报错  
Resources根据名称去查找,默认情况定义的变量名就是查找的名称,也可以手动指定  
当一个类存在多个实例时,就使用Resources  
如果多实例使用auotwired,则需要增加一个Qualifier注解指定对象的变量名

主类
```java
package SpringIocDemo.AutoInject;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class AutoMain {
    public static void main(String[] args) {
        AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(Config.class);
//        FileSystemXmlApplicationContext cont = new FileSystemXmlApplicationContext("D:\\Code\\Java\\AllDemo\\Learn\\src\\main\\java\\SpringIocDemo\\AutoInject\\spring.xml");
        UserInter users = context.getBean(UserService.class);

        System.out.println(users.getALlUser());
    }
}
```
使用 @ComponentScan 配置扫瞄的包或者类
```java
package SpringIocDemo.AutoInject;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
@Configuration
@ComponentScan(basePackages = "SpringIocDemo.AutoInject" )
public class Config {

}
```
目标类
```java
package SpringIocDemo.AutoInject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import java.util.ArrayList;
import java.util.List;
@Controller
public class UserService implements UserInter{

    @Autowired
    Cat cat;
    @Autowired
    Cat cat2;

    @Override
    public List<String> getALlUser(){
        ArrayList<String> users = new ArrayList<>();
        for(int i=0;i<10;i++){
            users.add("javaboy:"+i);
        }
        cat.setAge(20);
        cat.setName("tes2");
        System.out.println(cat.toString());
        cat2.setAge(22);
        cat2.setName("test4");
        System.out.println(cat.toString());
        return users;
    }
}

```
xml配置扫瞄包或者类
```xml
 <context:component-scan base-package="SpringIocDemo.AutoInject"/>
```
# 6.@Condition条件注解
即根据条件来选择获取的对象或者执行的代码  

步骤
1. 创建条件类,实现 Condition 接口
2. 定义目标实例类
3. 配置bean,需要使用相同的ID,并使用 @Conditional 注解

条件类
```java
package SpringIocDemo.ConditionDemo;

import org.springframework.context.annotation.Condition;
import org.springframework.context.annotation.ConditionContext;
import org.springframework.core.type.AnnotatedTypeMetadata;

import java.util.Locale;

public class LinuxCondition implements Condition {

    @Override
    public boolean matches(ConditionContext conditionContext, AnnotatedTypeMetadata annotatedTypeMetadata) {
        return conditionContext.getEnvironment().getProperty("os.name").toLowerCase(Locale.ROOT).contains("linux");
    }
}

```
```java
package SpringIocDemo.ConditionDemo;

import org.springframework.context.annotation.Condition;
import org.springframework.context.annotation.ConditionContext;
import org.springframework.core.type.AnnotatedTypeMetadata;

public class WinCondition implements Condition {

    @Override
    public boolean matches(ConditionContext conditionContext, AnnotatedTypeMetadata annotatedTypeMetadata) {
        return conditionContext.getEnvironment().getProperty("os.name").toLowerCase().contains("windows");
    }
}

```
实例类接口
```java
package SpringIocDemo.ConditionDemo;


public interface ShowCmd {
    public void showCmd();
}

```
实例类
```java
package SpringIocDemo.ConditionDemo;

public class WinShowCmd implements ShowCmd {
    @Override
    public void showCmd() {
        System.out.println("dir");
    }
}

```
```java
package SpringIocDemo.ConditionDemo;

public class LinuxShowCmd implements ShowCmd {
    @Override
    public void showCmd() {
        System.out.println("ls");
    }
}

```
配置类
```java
package SpringIocDemo.ConditionDemo;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Conditional;
import org.springframework.context.annotation.Configuration;

@Configuration
public class Config {
    @Bean("cmd")
    @Conditional(WinCondition.class)
    ShowCmd winCmd(){
        return new WinShowCmd();
    }
    @Bean("cmd")
    @Conditional(LinuxCondition.class)
    ShowCmd linuxcmd(){
        return new LinuxShowCmd();
    }
}

```
主类调用方式
```java
package SpringIocDemo.ConditionDemo;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class ConditionMain {
    public static void main(String[] args) {
        AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(Config.class);
        ShowCmd cmd = context.getBean("cmd",ShowCmd.class);
        // 这里会根据对应的条件执行bean内对应的方法
        cmd.showCmd();
    }
}

```
