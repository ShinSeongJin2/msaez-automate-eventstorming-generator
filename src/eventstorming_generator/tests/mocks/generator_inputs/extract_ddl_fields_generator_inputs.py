extract_ddl_fields_generator_inputs = {
    "ddl": """
-- Create table
create table EXHR.IS_TAKEOVER_INFO
(
  host_empcd          VARCHAR2(8),
  host_hname          VARCHAR2(50),
  host_emp_id         NUMBER,
  host_s_empcd        NUMBER,
  t_hname             VARCHAR2(50),
  t_empcd             VARCHAR2(30),
  com1                VARCHAR2(1),
  com2                VARCHAR2(1),
  com3                VARCHAR2(1),
  com4                VARCHAR2(1),
  com5                VARCHAR2(1),
  com6                VARCHAR2(1),
  com7                VARCHAR2(1),
  com8                VARCHAR2(100),
  status              VARCHAR2(1),
  mail_send_id_h      NUMBER,
  mail_key            VARCHAR2(30),
  mail_msg            CLOB,
  start_date          DATE,
  end_date            DATE,
  takeover_detail     VARCHAR2(3000),
  message_center_flag VARCHAR2(1) default 'N',
  title               VARCHAR2(200),
  reject_message      VARCHAR2(200),
  create_date         DATE,
  create_by           VARCHAR2(8),
  update_date         DATE,
  update_by           VARCHAR2(8)
)
tablespace EX_HR_DATA
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 128K
    next 128K
    minextents 1
    maxextents unlimited
  );
-- Add comments to the columns 
comment on column EXHR.IS_TAKEOVER_INFO.host_empcd
  is '인계자 사번';
comment on column EXHR.IS_TAKEOVER_INFO.host_hname
  is '인계자 이름';
comment on column EXHR.IS_TAKEOVER_INFO.host_emp_id
  is '인계자 직원 ID';
comment on column EXHR.IS_TAKEOVER_INFO.host_s_empcd
  is '인계자 상위직책자 사번';
comment on column EXHR.IS_TAKEOVER_INFO.t_hname
  is '인수자 이름';
comment on column EXHR.IS_TAKEOVER_INFO.t_empcd
  is '인수자 사번';
comment on column EXHR.IS_TAKEOVER_INFO.com1
  is '기본 업무 현황 여부 (1:완료, 2: 해당없음)';
comment on column EXHR.IS_TAKEOVER_INFO.com2
  is '인원현황,업무분장표 여부 (1:완료, 2: 해당없음)';
comment on column EXHR.IS_TAKEOVER_INFO.com3
  is '시설장비,비품,자재현황 여부 (1:완료, 2: 해당없음)';
comment on column EXHR.IS_TAKEOVER_INFO.com4
  is '연도 목표, 예산 및 집행실적 (1:완료, 2: 해당없음)';
comment on column EXHR.IS_TAKEOVER_INFO.com5
  is '영업 또는 프로젝트 진행 현황 (1:완료, 2: 해당없음)';
comment on column EXHR.IS_TAKEOVER_INFO.com6
  is '문서, 도서와 자료 현황 (1:완료, 2: 해당없음)';
comment on column EXHR.IS_TAKEOVER_INFO.com7
  is '진행과 미결사항 (1:완료, 2: 해당없음)';
comment on column EXHR.IS_TAKEOVER_INFO.com8
  is '기타';
comment on column EXHR.IS_TAKEOVER_INFO.status
  is '인수인계 상태 (0 : 인계자 등록 / 1 : 인수자 확인 / 2 : 인수자 반려 / 3 : 최종 결재 완료 / 4 : 상급자 반려),IS_SY02(CODETP =''E630'')';
comment on column EXHR.IS_TAKEOVER_INFO.mail_send_id_h
  is '메일발송 ID(From IS_ASSIGNMENT_MAIL_SEND_LOG.MAIL_SEND_ID_H), 값이 없을경우 발령무관 생성 인수인계 건';
comment on column EXHR.IS_TAKEOVER_INFO.mail_key
  is '메일 로그 ID';
comment on column EXHR.IS_TAKEOVER_INFO.mail_msg
  is '인수인계 View 생성용';
comment on column EXHR.IS_TAKEOVER_INFO.start_date
  is '시작일';
comment on column EXHR.IS_TAKEOVER_INFO.end_date
  is '종료일(최종결재시)';
comment on column EXHR.IS_TAKEOVER_INFO.takeover_detail
  is '인수인계 상세 내용';
comment on column EXHR.IS_TAKEOVER_INFO.message_center_flag
  is '메시지 센터 구분용(Y : 확인, N : 미확인)';
comment on column EXHR.IS_TAKEOVER_INFO.title
  is '인수인계 제목';
comment on column EXHR.IS_TAKEOVER_INFO.reject_message
  is '인수인계 반려 문구';
-- Create/Recreate indexes 
create index EXHR.IS_TAKEOVER_INFO_N1 on EXHR.IS_TAKEOVER_INFO (MAIL_SEND_ID_H)
  tablespace EX_HR_INDEX
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
create index EXHR.IS_TAKEOVER_INFO_N2 on EXHR.IS_TAKEOVER_INFO (HOST_EMPCD)
  tablespace EX_HR_INDEX
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
create index EXHR.IS_TAKEOVER_INFO_N3 on EXHR.IS_TAKEOVER_INFO (HOST_EMP_ID)
  tablespace EX_HR_INDEX
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
-- Create table
create table EXHR.IS_ASSIGNMENT_MAIL_SEND_LOG_D
(
  mail_send_id_h    NUMBER not null,
  mail_send_id      NUMBER not null,
  emp_id            NUMBER not null,
  bal_section       VARCHAR2(100),
  balgb             VARCHAR2(100),
  description       VARCHAR2(3000),
  baldate_from      DATE,
  baldate_to        DATE,
  last_update_date  DATE,
  last_updated_by   NUMBER(15),
  last_update_login NUMBER(15),
  created_by        NUMBER(15),
  creation_date     DATE
)
tablespace EX_HR_DATA
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
-- Add comments to the table 
comment on table EXHR.IS_ASSIGNMENT_MAIL_SEND_LOG_D
  is '인수인계 메일발송- 발령연계정보';
-- Add comments to the columns 
comment on column EXHR.IS_ASSIGNMENT_MAIL_SEND_LOG_D.mail_send_id_h
  is 'IS_ASSIGNMENT_MAIL_SEND_LOG.MAIL_SEND_ID_H';
comment on column EXHR.IS_ASSIGNMENT_MAIL_SEND_LOG_D.mail_send_id
  is 'IS_PE31.MAIL_SEND_ID';
comment on column EXHR.IS_ASSIGNMENT_MAIL_SEND_LOG_D.bal_section
  is '발령구분코드, IS_PE31.BAL_SECTION';
comment on column EXHR.IS_ASSIGNMENT_MAIL_SEND_LOG_D.balgb
  is '발령유형코드, IS_PE31.BAL_GB';
comment on column EXHR.IS_ASSIGNMENT_MAIL_SEND_LOG_D.description
  is '발령내용,IS_PE31.DESCRIPTION';
comment on column EXHR.IS_ASSIGNMENT_MAIL_SEND_LOG_D.baldate_from
  is '발령시작일,IS_PE31.BALDATE_FROM';
comment on column EXHR.IS_ASSIGNMENT_MAIL_SEND_LOG_D.baldate_to
  is '발령종료일,IS_PE31.BALDATE_TO';

"""
}