Name:           caffeine
Version:        2.3.3
Release:        0%{?dist}
Summary:        High performance, near optimal caching library based on Java 8

License:        ASL 2.0
URL:            https://github.com/ben-manes/%{name}
Source0:        https://github.com/ben-manes/%{name}/archive/v%{version}.tar.gz
Source1:	https://repo1.maven.org/maven2/com/github/ben-manes/%{name}/%{name}/%{version}/%{name}-%{version}.pom

# remove jacoco and coveralls
#Patch0:         %%{name}-build.patch

BuildArch:      noarch

# build
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(org.apache.felix:org.apache.felix.framework)
BuildRequires:  mvn(org.testng:testng)
BuildRequires:  mvn(org.jctools:jctools-core)
BuildRequires:  mvn(com.google.guava:guava-testlib)
# missing test dependencies
#BuildRequires:  mvn(org.hamcrest:java-hamcrest)
#BuildRequires:  mvn(org.awaitility:awaitility)
#BuildRequires:  mvn(org.ops4j.pax.exam:pax-exam-junit4)
#BuildRequires:  mvn(com.github.brianfrankcooper.ycsb:core)
#BuildRequires:  mvn(org.ops4j.pax.exam:pax-exam-container-native)
#BuildRequires:  mvn(org.ops4j.pax.exam:pax-exam-link-mvn)
#BuildRequires:  mvn(org.ops4j.pax.url:pax-url-aether)
# missing depenedencies
#BuildRequires:  mvn(com.google.errorprone:error_prone_annotations)

%description
A Cache is similar to ConcurrentMap, but not quite the same. The most
fundamental difference is that a ConcurrentMap persists all elements that are
added to it until they are explicitly removed. A Cache on the other hand is
generally configured to evict entries automatically, in order to constrain its
memory footprint. In some cases a LoadingCache or AsyncLoadingCache can be
useful even if it doesn't evict entries, due to its automatic cache loading.

Caffeine provide flexible construction to create a cache with a combination
of the following features:
automatic loading of entries into the cache, optionally asynchronously
size-based eviction when a maximum is exceeded based on frequency and recency
time-based expiration of entries, measured since last access or last write
asynchronously refresh when the first stale request for an entry occurs
keys automatically wrapped in weak references
values automatically wrapped in weak or soft references
notification of evicted (or otherwise removed) entries
writes propagated to an external resource
accumulation of cache access statistics

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

cp -p %{SOURCE1} pom.xml

%pom_xpath_inject "pom:project" "<properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>"

%pom_xpath_inject "pom:project" "<build>
    <directory>target</directory>
    <outputDirectory>target/classes</outputDirectory>
    <finalName>${artifactId}-${version}</finalName>
    <testOutputDirectory>target/test-classes</testOutputDirectory>
    <sourceDirectory>caffeine/src/main/java</sourceDirectory>
    <testSourceDirectory>caffeine/src/test/java</testSourceDirectory>
    <resources>
      <resource>
        <directory>caffeine/src/main</directory>
      </resource>
    </resources>
    <testResources>
      <testResource>
        <directory>caffeine/src/test</directory>
      </testResource>
    </testResources>
    <pluginManagement>
      <plugins>
	<plugin>
          <artifactId>maven-compiler-plugin</artifactId>
          <version>2.3.2</version>
	  <configuration>
            <source>1.8</source>
            <target>1.8</target>
	    <showDeprecation>true</showDeprecation>
          </configuration>
        </plugin>
      </plugins>
    </pluginManagement>
  </build>"

# remove test dependencies
%pom_remove_dep org.hamcrest:java-hamcrest
%pom_remove_dep org.awaitility:awaitility
%pom_remove_dep org.ops4j.pax.exam:pax-exam-junit4
%pom_remove_dep com.github.brianfrankcooper.ycsb:core
%pom_remove_dep org.ops4j.pax.exam:pax-exam-container-native
%pom_remove_dep org.ops4j.pax.exam:pax-exam-link-mvn
%pom_remove_dep org.ops4j.pax.url:pax-url-aether

# try to remove missing dependencies
%pom_remove_dep com.google.errorprone:error_prone_annotations

# remove files using optional dependencies

%build
%mvn_build

%install
%mvn_install 

%files -f .mfiles
%doc README.md
%license LICENSE

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
