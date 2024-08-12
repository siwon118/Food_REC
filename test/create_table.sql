drop database if exists capstone;
create database capstone;
show databases;
use capstone;

drop table if exists users; 			-- 사용자 테이블
drop table if exists allergy; 			-- 사용자 알레르기 테이블
drop table if exists list; 				-- 섭취 식단 리스트 테이블
drop table if exists food; 				-- 음식 정보 테이블
drop table if exists food_nutrients; 	-- 음식 영양성분 테이블

create table users(
userid varchar(20) not null,				-- 사용자 id
passwd varchar(16) not null,				-- 사용자 password
fd_preference varchar(100) default null,	-- 사용자 선호 식자재
primary key(userid) using btree
)
collate = 'utf8mb4_general_ci'
engine = InnoDB ;

create table allergy(
userid varchar(20) not null,	-- 사용자 id
allergy char(100) default null,	-- 보유 알레르기 정보
primary key(userid) using btree
)
collate = 'utf8mb4_general_ci'
engine = InnoDB ;

create table list(
userid varchar(20) not null,	-- 사용자 id
intakedt date not null,			-- 섭취 날짜
fd_code char(7) not null,		-- 음식 코드
fd_name char(100) not null,		-- 음식 이름
energy float default 0,			-- 열량(칼로리)
prot float default 0,				-- 단백질
fibtg float default 0,			-- 식이섬유
vitc float default 0,				-- 비타민C
vite float default 0,				-- 비타민E
vitb1 float default 0,			-- 비타민B1
vitb2 float default 0,			-- 비타민B2
vitb6 float default 0,			-- 비타민B6
vitb12 float default 0,			-- 비타민B12
nacn float default 0,				-- 나이아신
clci float default 0,				-- 칼슘
na float default 0, 				-- 나트륨
zn float default 0,				-- 아연
primary key(userid) using btree
)
collate = 'utf8mb4_general_ci'
engine = InnoDB 
;

create table food(
fd_code char(7) not null,			-- 음식 코드
fd_name char(100) not null,			-- 음식 이름
fd_ingredients char(100) not null,	-- 식자재명
fd_allergy char(100) default null,	-- 식자재별 알레르기 정보
primary key(fd_code) using btree
)
collate = 'utf8mb4_general_ci'
engine = InnoDB 
;

create table food_nutrients(
fd_code char(7) not null,		-- 음식 코드
energy float default 0,			-- 열량(칼로리)
prot float default 0,				-- 단백질
fibtg float default 0,			-- 식이섬유
vitc float default 0,				-- 비타민C
vite float default 0,				-- 비타민E
vitb1 float default 0,			-- 비타민B1
vitb2 float default 0,			-- 비타민B2
vitb6 float default 0,			-- 비타민B6
vitb12 float default 0,			-- 비타민B12
nacn float default 0,				-- 나이아신
clci float default 0,				-- 칼슘
na float default 0, 				-- 나트륨
zn float default 0,				-- 아연
primary key(fd_code) using btree
)
collate = 'utf8mb4_general_ci'
engine = InnoDB 
;
select * from users;
select * from allergy;
select * from list;
select * from food;
select * from food_nutrients;

