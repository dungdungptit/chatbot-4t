from getpass import getpass
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

from langchain.prompts import ChatPromptTemplate

""" 
--
Nếu câu trả lời có link ảnh (type: image) hoặc link đường dẫn, hãy sử dụng dấu gạch chân (_) theo cú pháp [ảnh](url) để thể hiện link ảnh hoặc [đường dẫn](url) link đường dẫn.
--
 """

# Update the template based on the type of SQL Database like MySQL, Microsoft SQL Server and so on
template = """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Given an input question, convert it to a SQL query. No pre-amble."),
        ("human", template),
    ]
)


def get_schema():
    db_get_table_info = ""
    with open("./database.sql", "r") as file:
        db_get_table_info = file.readlines()
        file.close()
    return """--BẢNG CHA
CREATE TABLE public.linh_vuc_tttt (
	id serial4 NOT NULL,
	"name" varchar NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT linh_vuc_tttt_pkey PRIMARY KEY (id)
);

CREATE TABLE public.loai (
	id serial4 NOT NULL,
	"name" varchar NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT loai_pkey PRIMARY KEY (id)
);

CREATE TABLE public.to_chuc_tieu_chuan (
	id serial4 NOT NULL,
	"name" varchar NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT to_chuc_tieu_chuan_pkey PRIMARY KEY (id)
);

CREATE TABLE public.ir_attachment (
	id serial4 NOT NULL,
	res_id int4 NULL,
	company_id int4 NULL,
	file_size int4 NULL,
	"name" varchar NOT NULL,
	res_model varchar NULL,
	res_field varchar NULL,
	"type" varchar NOT NULL,
	url varchar(1024) NULL,
	access_token varchar NULL,
	store_fname varchar NULL,
	checksum varchar(40) NULL,
	mimetype varchar NULL,
	description text NULL,
	index_content text NULL,
	public bool NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	db_datas bytea NULL,
	original_id int4 NULL,
	CONSTRAINT ir_attachment_pkey PRIMARY KEY (id),
	CONSTRAINT ir_attachment_original_id_fkey FOREIGN KEY (original_id) REFERENCES public.ir_attachment(id) ON DELETE SET NULL
);
CREATE INDEX ir_attachment__store_fname_index ON public.ir_attachment USING btree (store_fname);
CREATE INDEX ir_attachment__url_index ON public.ir_attachment USING btree (url) WHERE (url IS NOT NULL);
CREATE INDEX ir_attachment_res_idx ON public.ir_attachment USING btree (res_model, res_id);

CREATE TABLE public.phan_cap (
	id serial4 NOT NULL,
	loai_id int4 NULL,
	phan_cap_cha_id int4 NULL,
	"name" varchar NULL,
	mo_ta varchar NULL,
	loai_phan_cap varchar NULL,
	ten_hien_thi varchar NULL,
	"key" text NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT phan_cap_pkey PRIMARY KEY (id),
	CONSTRAINT phan_cap_loai_id_fkey FOREIGN KEY (loai_id) REFERENCES public.loai(id) ON DELETE SET NULL,
	CONSTRAINT phan_cap_phan_cap_cha_id_fkey FOREIGN KEY (phan_cap_cha_id) REFERENCES public.phan_cap(id) ON DELETE CASCADE
);

CREATE TABLE public.co_quan (
	id serial4 NOT NULL,
	"name" varchar NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT co_quan_pkey PRIMARY KEY (id)
);

CREATE TABLE public.phong_thu_nghiem (
	id serial4 NOT NULL,
	"name" varchar NULL,
	address varchar NULL,
	so_quyet_dinh varchar NULL,
	email varchar NULL,
	phone_number varchar NULL,
	ngay_quyet_dinh date NULL,
	han_chi_dinh date NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT phong_thu_nghiem_pkey PRIMARY KEY (id)
);

CREATE TABLE public.lifecycle (
	id serial4 NOT NULL,
	"name" varchar NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT lifecycle_pkey PRIMARY KEY (id)
);

CREATE TABLE public.chuyen_gia (
	id serial4 NOT NULL,
	"name" varchar NULL,
	address varchar NULL,
	phone_number varchar NULL,
	email varchar NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT chuyen_gia_pkey PRIMARY KEY (id)
);

CREATE TABLE public.linh_vuc (
	id serial4 NOT NULL,
	"name" varchar NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT linh_vuc_pkey PRIMARY KEY (id)
);

CREATE TABLE public.wizard_search_tieu_chuan (
	id serial4 NOT NULL,
	search_data varchar NULL,
	search_data1 varchar NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT wizard_search_tieu_chuan_pkey PRIMARY KEY (id)
);

--BẢNG CHÍNH
CREATE TABLE public.tcvn (
	id serial4 NOT NULL,
	to_chuc_tieu_chuan_id int4 NULL,
	loai_id int4 NULL,
	linh_vuc_tttt int4 NULL,
	so_hieu varchar NOT NULL,
	ten_tieng_viet varchar NULL,
	ten_tieng_anh varchar NULL,
	nam_ban_hanh_char varchar NULL,
	duong_link varchar NULL,
	so_van_ban_cong_bo varchar NULL,
	co_quan_cong_bo varchar NULL,
	co_quan_xay_dung varchar NULL,
	phan_loai varchar NULL,
	loai_hinh varchar NULL,
	trang_thai varchar NOT NULL,
	trang_thai_duyet varchar NULL,
	trang_thai_khoi_tao varchar NULL,
	loai varchar NULL,
	ma_so_de_tai_lien_quan varchar NULL,
	ghi_chu varchar NULL,
	phien_ban varchar NULL,
	lifecycle varchar NULL,
	time_lifecycle date NULL,
	mo_ta text NULL,
	search_all text NULL,
	check_cong_khai bool NULL,
	nam_ban_hanh timestamp NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT tcvn_pkey PRIMARY KEY (id),
	CONSTRAINT tcvn_linh_vuc_tttt_fkey FOREIGN KEY (linh_vuc_tttt) REFERENCES public.linh_vuc_tttt(id) ON DELETE SET NULL,
	CONSTRAINT tcvn_loai_id_fkey FOREIGN KEY (loai_id) REFERENCES public.loai(id) ON DELETE SET NULL,
	CONSTRAINT tcvn_to_chuc_tieu_chuan_id_fkey FOREIGN KEY (to_chuc_tieu_chuan_id) REFERENCES public.to_chuc_tieu_chuan(id) ON DELETE SET NULL
);

CREATE TABLE public.qcvn (
	id serial4 NOT NULL,
	to_chuc_tieu_chuan_id int4 NULL,
	linh_vuc_tttt int4 NULL,
	co_quan_bien_soan int4 NULL,
	co_quan_ban_hanh int4 NULL,
	loai_id int4 NULL,
	duong_link varchar NULL,
	trang_thai_duyet varchar NULL,
	loai varchar NULL,
	thong_tu_ban_hanh varchar NULL,
	pham_vi_ap_dung varchar NULL,
	so_hieu varchar NOT NULL,
	ten_tieng_viet varchar NULL,
	ten_tieng_anh varchar NULL,
	nam_ban_hanh varchar NULL,
	so_van_ban_cong_bo varchar NULL,
	co_quan_cong_bo varchar NULL,
	co_quan_xay_dung varchar NULL,
	phan_loai varchar NULL,
	loai_hinh varchar NULL,
	trang_thai varchar NOT NULL,
	ma_so_de_tai_lien_quan varchar NULL,
	ghi_chu varchar NULL,
	mo_ta text NULL,
	search_all text NULL,
	check_cong_khai bool NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT qcvn_pkey PRIMARY KEY (id),
	CONSTRAINT qcvn_co_quan_ban_hanh_fkey FOREIGN KEY (co_quan_ban_hanh) REFERENCES public.co_quan(id) ON DELETE SET NULL,
	CONSTRAINT qcvn_co_quan_bien_soan_fkey FOREIGN KEY (co_quan_bien_soan) REFERENCES public.co_quan(id) ON DELETE SET NULL,
	CONSTRAINT qcvn_linh_vuc_tttt_fkey FOREIGN KEY (linh_vuc_tttt) REFERENCES public.linh_vuc_tttt(id) ON DELETE SET NULL,
	CONSTRAINT qcvn_loai_id_fkey FOREIGN KEY (loai_id) REFERENCES public.loai(id) ON DELETE SET NULL,
	CONSTRAINT qcvn_to_chuc_tieu_chuan_id_fkey FOREIGN KEY (to_chuc_tieu_chuan_id) REFERENCES public.to_chuc_tieu_chuan(id) ON DELETE SET NULL
);

--BẢNG CON CHUNG
CREATE TABLE public.du_lieu_them (
	id serial4 NOT NULL,
	qcvn_id int4 NULL,
	tcvn_id int4 NULL,
	ten_hien_thi varchar NULL,
	"key" varchar NULL,
	value varchar NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT du_lieu_them_pkey PRIMARY KEY (id),
	CONSTRAINT du_lieu_them_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE SET NULL,
	CONSTRAINT du_lieu_them_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE SET NULL
);

CREATE TABLE public.tai_lieu_lien_quan (
	id serial4 NOT NULL,
	tieu_chuan_id int4 NULL,
	quy_chuan_id int4 NULL,
	ke_hoach_xay_dung varchar NULL,
	xin_y_kien varchar NULL,
	tham_tra varchar NULL,
	gui_tham_dinh varchar NULL,
	cong_bo_ban_hanh varchar NULL,
	van_ban_cong_bo_ban_hanh varchar NULL,
	create_date timestamp NULL,
	write_date timestamp NULL,
	CONSTRAINT tai_lieu_lien_quan_pkey PRIMARY KEY (id),
	CONSTRAINT tai_lieu_lien_quan_quy_chuan_id_fkey FOREIGN KEY (quy_chuan_id) REFERENCES public.qcvn(id) ON DELETE SET NULL,
	CONSTRAINT tai_lieu_lien_quan_tieu_chuan_id_fkey FOREIGN KEY (tieu_chuan_id) REFERENCES public.tcvn(id) ON DELETE SET NULL
);

CREATE TABLE public.tcvn_vien_dan (
	qcvn_id int4 NOT NULL,
	tcvn_id int4 NOT NULL,
	CONSTRAINT tcvn_vien_dan_pkey PRIMARY KEY (qcvn_id, tcvn_id),
	CONSTRAINT tcvn_vien_dan_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE,
	CONSTRAINT tcvn_vien_dan_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX tcvn_vien_dan_tcvn_id_qcvn_id_idx ON public.tcvn_vien_dan USING btree (tcvn_id, qcvn_id);

CREATE TABLE public.rel_qcvn_thay_the_cho (
	qcvn_id int4 NOT NULL,
	tcvn_id int4 NOT NULL,
	CONSTRAINT rel_qcvn_thay_the_cho_pkey PRIMARY KEY (qcvn_id, tcvn_id),
	CONSTRAINT rel_qcvn_thay_the_cho_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE,
	CONSTRAINT rel_qcvn_thay_the_cho_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_qcvn_thay_the_cho_tcvn_id_qcvn_id_idx ON public.rel_qcvn_thay_the_cho USING btree (tcvn_id, qcvn_id);

CREATE TABLE public.rel_qcvn_tai_lieu_tham_chieu (
	qcvn_id int4 NOT NULL,
	tcvn_id int4 NOT NULL,
	CONSTRAINT rel_qcvn_tai_lieu_tham_chieu_pkey PRIMARY KEY (qcvn_id, tcvn_id),
	CONSTRAINT rel_qcvn_tai_lieu_tham_chieu_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE,
	CONSTRAINT rel_qcvn_tai_lieu_tham_chieu_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_qcvn_tai_lieu_tham_chieu_tcvn_id_qcvn_id_idx ON public.rel_qcvn_tai_lieu_tham_chieu USING btree (tcvn_id, qcvn_id);

CREATE TABLE public.rel_qcvn_tieu_chuan_tuong_duong (
	qcvn_id int4 NOT NULL,
	tcvn_id int4 NOT NULL,
	CONSTRAINT rel_qcvn_tieu_chuan_tuong_duong_pkey PRIMARY KEY (qcvn_id, tcvn_id),
	CONSTRAINT rel_qcvn_tieu_chuan_tuong_duong_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE,
	CONSTRAINT rel_qcvn_tieu_chuan_tuong_duong_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_qcvn_tieu_chuan_tuong_duong_tcvn_id_qcvn_id_idx ON public.rel_qcvn_tieu_chuan_tuong_duong USING btree (tcvn_id, qcvn_id);

CREATE TABLE public.tcvn_tham_chieu (
	qcvn_id int4 NOT NULL,
	tcvn_id int4 NOT NULL,
	CONSTRAINT tcvn_tham_chieu_pkey PRIMARY KEY (qcvn_id, tcvn_id),
	CONSTRAINT tcvn_tham_chieu_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE,
	CONSTRAINT tcvn_tham_chieu_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX tcvn_tham_chieu_tcvn_id_qcvn_id_idx ON public.tcvn_tham_chieu USING btree (tcvn_id, qcvn_id);

CREATE TABLE public.rel_qcvn_thay_the_boi (
	qcvn_id int4 NOT NULL,
	tcvn_id int4 NOT NULL,
	CONSTRAINT rel_qcvn_thay_the_boi_pkey PRIMARY KEY (qcvn_id, tcvn_id),
	CONSTRAINT rel_qcvn_thay_the_boi_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE,
	CONSTRAINT rel_qcvn_thay_the_boi_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_qcvn_thay_the_boi_tcvn_id_qcvn_id_idx ON public.rel_qcvn_thay_the_boi USING btree (tcvn_id, qcvn_id);

-- BẢNG CON RIÊNG CỦA TIÊU CHUẨN
CREATE TABLE public.tcvn_thay_the_cho (
	tcvn1 int4 NOT NULL,
	tcvn2 int4 NOT NULL,
	CONSTRAINT tcvn_thay_the_cho_pkey PRIMARY KEY (tcvn1, tcvn2),
	CONSTRAINT tcvn_thay_the_cho_tcvn1_fkey FOREIGN KEY (tcvn1) REFERENCES public.tcvn(id) ON DELETE CASCADE,
	CONSTRAINT tcvn_thay_the_cho_tcvn2_fkey FOREIGN KEY (tcvn2) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX tcvn_thay_the_cho_tcvn2_tcvn1_idx ON public.tcvn_thay_the_cho USING btree (tcvn2, tcvn1);

CREATE TABLE public.tcvn_tai_lieu_tham_chieu (
	tcvn1 int4 NOT NULL,
	tcvn2 int4 NOT NULL,
	CONSTRAINT tcvn_tai_lieu_tham_chieu_pkey PRIMARY KEY (tcvn1, tcvn2),
	CONSTRAINT tcvn_tai_lieu_tham_chieu_tcvn1_fkey FOREIGN KEY (tcvn1) REFERENCES public.tcvn(id) ON DELETE CASCADE,
	CONSTRAINT tcvn_tai_lieu_tham_chieu_tcvn2_fkey FOREIGN KEY (tcvn2) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX tcvn_tai_lieu_tham_chieu_tcvn2_tcvn1_idx ON public.tcvn_tai_lieu_tham_chieu USING btree (tcvn2, tcvn1);

CREATE TABLE public.tcvn_tieu_chuan_tuong_duong (
	tcvn1 int4 NOT NULL,
	tcvn2 int4 NOT NULL,
	CONSTRAINT tcvn_tieu_chuan_tuong_duong_pkey PRIMARY KEY (tcvn1, tcvn2),
	CONSTRAINT tcvn_tieu_chuan_tuong_duong_tcvn1_fkey FOREIGN KEY (tcvn1) REFERENCES public.tcvn(id) ON DELETE CASCADE,
	CONSTRAINT tcvn_tieu_chuan_tuong_duong_tcvn2_fkey FOREIGN KEY (tcvn2) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX tcvn_tieu_chuan_tuong_duong_tcvn2_tcvn1_idx ON public.tcvn_tieu_chuan_tuong_duong USING btree (tcvn2, tcvn1);

CREATE TABLE public.tcvn_thay_the_boi (
	tcvn1 int4 NOT NULL,
	tcvn2 int4 NOT NULL,
	CONSTRAINT tcvn_thay_the_boi_pkey PRIMARY KEY (tcvn1, tcvn2),
	CONSTRAINT tcvn_thay_the_boi_tcvn1_fkey FOREIGN KEY (tcvn1) REFERENCES public.tcvn(id) ON DELETE CASCADE,
	CONSTRAINT tcvn_thay_the_boi_tcvn2_fkey FOREIGN KEY (tcvn2) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX tcvn_thay_the_boi_tcvn2_tcvn1_idx ON public.tcvn_thay_the_boi USING btree (tcvn2, tcvn1);

CREATE TABLE public.lifecycle_tcvn_rel (
	tcvn_id int4 NOT NULL,
	lifecycle_id int4 NOT NULL,
	CONSTRAINT lifecycle_tcvn_rel_pkey PRIMARY KEY (tcvn_id, lifecycle_id),
	CONSTRAINT lifecycle_tcvn_rel_lifecycle_id_fkey FOREIGN KEY (lifecycle_id) REFERENCES public.lifecycle(id) ON DELETE CASCADE,
	CONSTRAINT lifecycle_tcvn_rel_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX lifecycle_tcvn_rel_lifecycle_id_tcvn_id_idx ON public.lifecycle_tcvn_rel USING btree (lifecycle_id, tcvn_id);

CREATE TABLE public.rel_tcvn_xin_y_kien (
	tcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT rel_tcvn_xin_y_kien_pkey PRIMARY KEY (tcvn_id, ir_attachment_id),
	CONSTRAINT rel_tcvn_xin_y_kien_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT rel_tcvn_xin_y_kien_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_tcvn_xin_y_kien_ir_attachment_id_tcvn_id_idx ON public.rel_tcvn_xin_y_kien USING btree (ir_attachment_id, tcvn_id);

CREATE TABLE public.rel_tieu_chuan_phan_cap (
	tieu_chuan_id int4 NOT NULL,
	phan_cap_id int4 NOT NULL,
	CONSTRAINT rel_tieu_chuan_phan_cap_pkey PRIMARY KEY (tieu_chuan_id, phan_cap_id),
	CONSTRAINT rel_tieu_chuan_phan_cap_phan_cap_id_fkey FOREIGN KEY (phan_cap_id) REFERENCES public.phan_cap(id) ON DELETE CASCADE,
	CONSTRAINT rel_tieu_chuan_phan_cap_tieu_chuan_id_fkey FOREIGN KEY (tieu_chuan_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_tieu_chuan_phan_cap_phan_cap_id_tieu_chuan_id_idx ON public.rel_tieu_chuan_phan_cap USING btree (phan_cap_id, tieu_chuan_id);

CREATE TABLE public.rel_tcvn_chuyen_vien (
	tcvn_id int4 NOT NULL,
	chuyen_gia_id int4 NOT NULL,
	CONSTRAINT rel_tcvn_chuyen_vien_pkey PRIMARY KEY (tcvn_id, chuyen_gia_id),
	CONSTRAINT rel_tcvn_chuyen_vien_chuyen_gia_id_fkey FOREIGN KEY (chuyen_gia_id) REFERENCES public.chuyen_gia(id) ON DELETE CASCADE,
	CONSTRAINT rel_tcvn_chuyen_vien_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_tcvn_chuyen_vien_chuyen_gia_id_tcvn_id_idx ON public.rel_tcvn_chuyen_vien USING btree (chuyen_gia_id, tcvn_id);

CREATE TABLE public.linh_vuc_tcvn_rel (
	tcvn_id int4 NOT NULL,
	linh_vuc_id int4 NOT NULL,
	CONSTRAINT linh_vuc_tcvn_rel_pkey PRIMARY KEY (tcvn_id, linh_vuc_id),
	CONSTRAINT linh_vuc_tcvn_rel_linh_vuc_id_fkey FOREIGN KEY (linh_vuc_id) REFERENCES public.linh_vuc(id) ON DELETE CASCADE,
	CONSTRAINT linh_vuc_tcvn_rel_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX linh_vuc_tcvn_rel_linh_vuc_id_tcvn_id_idx ON public.linh_vuc_tcvn_rel USING btree (linh_vuc_id, tcvn_id);

CREATE TABLE public.rel_phong_thu_nhiem_tcvn (
	phong_thu_nghiem_id int4 NOT NULL,
	tcvn_id int4 NOT NULL,
	CONSTRAINT rel_phong_thu_nhiem_tcvn_pkey PRIMARY KEY (phong_thu_nghiem_id, tcvn_id),
	CONSTRAINT rel_phong_thu_nhiem_tcvn_phong_thu_nghiem_id_fkey FOREIGN KEY (phong_thu_nghiem_id) REFERENCES public.phong_thu_nghiem(id) ON DELETE CASCADE,
	CONSTRAINT rel_phong_thu_nhiem_tcvn_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_phong_thu_nhiem_tcvn_tcvn_id_phong_thu_nghiem_id_idx ON public.rel_phong_thu_nhiem_tcvn USING btree (tcvn_id, phong_thu_nghiem_id);

CREATE TABLE public.rel_tcvn_van_ban_cong_bo_ban_hanh (
	tcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT rel_tcvn_van_ban_cong_bo_ban_hanh_pkey PRIMARY KEY (tcvn_id, ir_attachment_id),
	CONSTRAINT rel_tcvn_van_ban_cong_bo_ban_hanh_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT rel_tcvn_van_ban_cong_bo_ban_hanh_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_tcvn_van_ban_cong_bo_ban_hanh_ir_attachment_id_tcvn_id_idx ON public.rel_tcvn_van_ban_cong_bo_ban_hanh USING btree (ir_attachment_id, tcvn_id);

CREATE TABLE public.ir_attachment_tcvn_rel (
	tcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT ir_attachment_tcvn_rel_pkey PRIMARY KEY (tcvn_id, ir_attachment_id),
	CONSTRAINT ir_attachment_tcvn_rel_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT ir_attachment_tcvn_rel_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX ir_attachment_tcvn_rel_ir_attachment_id_tcvn_id_idx ON public.ir_attachment_tcvn_rel USING btree (ir_attachment_id, tcvn_id);

CREATE TABLE public.rel_tcvn_ke_hoach_xay_dung (
	tcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT rel_tcvn_ke_hoach_xay_dung_pkey PRIMARY KEY (tcvn_id, ir_attachment_id),
	CONSTRAINT rel_tcvn_ke_hoach_xay_dung_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT rel_tcvn_ke_hoach_xay_dung_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_tcvn_ke_hoach_xay_dung_ir_attachment_id_tcvn_id_idx ON public.rel_tcvn_ke_hoach_xay_dung USING btree (ir_attachment_id, tcvn_id);

CREATE TABLE public.rel_tieu_chuan_viet_nam_phan_cap (
	phan_cap_id int4 NOT NULL,
	tcvn_id int4 NOT NULL,
	CONSTRAINT rel_tieu_chuan_viet_nam_phan_cap_pkey PRIMARY KEY (phan_cap_id, tcvn_id),
	CONSTRAINT rel_tieu_chuan_viet_nam_phan_cap_phan_cap_id_fkey FOREIGN KEY (phan_cap_id) REFERENCES public.phan_cap(id) ON DELETE CASCADE,
	CONSTRAINT rel_tieu_chuan_viet_nam_phan_cap_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_tieu_chuan_viet_nam_phan_cap_tcvn_id_phan_cap_id_idx ON public.rel_tieu_chuan_viet_nam_phan_cap USING btree (tcvn_id, phan_cap_id);

CREATE TABLE public.rel_tieu_chuan_quoc_te_phan_cap (
	phan_cap_id int4 NOT NULL,
	tcvn_id int4 NOT NULL,
	CONSTRAINT rel_tieu_chuan_quoc_te_phan_cap_pkey PRIMARY KEY (phan_cap_id, tcvn_id),
	CONSTRAINT rel_tieu_chuan_quoc_te_phan_cap_phan_cap_id_fkey FOREIGN KEY (phan_cap_id) REFERENCES public.phan_cap(id) ON DELETE CASCADE,
	CONSTRAINT rel_tieu_chuan_quoc_te_phan_cap_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_tieu_chuan_quoc_te_phan_cap_tcvn_id_phan_cap_id_idx ON public.rel_tieu_chuan_quoc_te_phan_cap USING btree (tcvn_id, phan_cap_id);

CREATE TABLE public.rel_tcvn_gui_tham_dinh (
	tcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT rel_tcvn_gui_tham_dinh_pkey PRIMARY KEY (tcvn_id, ir_attachment_id),
	CONSTRAINT rel_tcvn_gui_tham_dinh_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT rel_tcvn_gui_tham_dinh_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_tcvn_gui_tham_dinh_ir_attachment_id_tcvn_id_idx ON public.rel_tcvn_gui_tham_dinh USING btree (ir_attachment_id, tcvn_id);

CREATE TABLE public.rel_tcvn_cong_bo_ban_hanh (
	tcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT rel_tcvn_cong_bo_ban_hanh_pkey PRIMARY KEY (tcvn_id, ir_attachment_id),
	CONSTRAINT rel_tcvn_cong_bo_ban_hanh_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT rel_tcvn_cong_bo_ban_hanh_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_tcvn_cong_bo_ban_hanh_ir_attachment_id_tcvn_id_idx ON public.rel_tcvn_cong_bo_ban_hanh USING btree (ir_attachment_id, tcvn_id);

CREATE TABLE public.rel_tcvn_tham_tra (
	tcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT rel_tcvn_tham_tra_pkey PRIMARY KEY (tcvn_id, ir_attachment_id),
	CONSTRAINT rel_tcvn_tham_tra_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT rel_tcvn_tham_tra_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_tcvn_tham_tra_ir_attachment_id_tcvn_id_idx ON public.rel_tcvn_tham_tra USING btree (ir_attachment_id, tcvn_id);

CREATE TABLE public.rel_tcvn_lanh_dao (
	tcvn_id int4 NOT NULL,
	chuyen_gia_id int4 NOT NULL,
	CONSTRAINT rel_tcvn_lanh_dao_pkey PRIMARY KEY (tcvn_id, chuyen_gia_id),
	CONSTRAINT rel_tcvn_lanh_dao_chuyen_gia_id_fkey FOREIGN KEY (chuyen_gia_id) REFERENCES public.chuyen_gia(id) ON DELETE CASCADE,
	CONSTRAINT rel_tcvn_lanh_dao_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_tcvn_lanh_dao_chuyen_gia_id_tcvn_id_idx ON public.rel_tcvn_lanh_dao USING btree (chuyen_gia_id, tcvn_id);

CREATE TABLE public.rel_wizard_search_tieu_chuan_quoc_te (
	wizard_search_tieu_chuan_id int4 NOT NULL,
	tcvn_id int4 NOT NULL,
	CONSTRAINT rel_wizard_search_tieu_chuan_quoc_te_pkey PRIMARY KEY (wizard_search_tieu_chuan_id, tcvn_id),
	CONSTRAINT rel_wizard_search_tieu_chuan_q_wizard_search_tieu_chuan_id_fkey FOREIGN KEY (wizard_search_tieu_chuan_id) REFERENCES public.wizard_search_tieu_chuan(id) ON DELETE CASCADE,
	CONSTRAINT rel_wizard_search_tieu_chuan_quoc_te_tcvn_id_fkey FOREIGN KEY (tcvn_id) REFERENCES public.tcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_wizard_search_tieu_chuan__tcvn_id_wizard_search_tieu_ch_idx ON public.rel_wizard_search_tieu_chuan_quoc_te USING btree (tcvn_id, wizard_search_tieu_chuan_id);


--BẢNG CON RIÊNG CỦA QUY CHUẨN
CREATE TABLE public.qcvn_vien_dan (
	qcvn1 int4 NOT NULL,
	qcvn2 int4 NOT NULL,
	CONSTRAINT qcvn_vien_dan_pkey PRIMARY KEY (qcvn1, qcvn2),
	CONSTRAINT qcvn_vien_dan_qcvn1_fkey FOREIGN KEY (qcvn1) REFERENCES public.qcvn(id) ON DELETE CASCADE,
	CONSTRAINT qcvn_vien_dan_qcvn2_fkey FOREIGN KEY (qcvn2) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX qcvn_vien_dan_qcvn2_qcvn1_idx ON public.qcvn_vien_dan USING btree (qcvn2, qcvn1);

CREATE TABLE public.rel_qcvn_van_ban_cong_bo_ban_hanh (
	qcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT rel_qcvn_van_ban_cong_bo_ban_hanh_pkey PRIMARY KEY (qcvn_id, ir_attachment_id),
	CONSTRAINT rel_qcvn_van_ban_cong_bo_ban_hanh_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT rel_qcvn_van_ban_cong_bo_ban_hanh_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_qcvn_van_ban_cong_bo_ban_hanh_ir_attachment_id_qcvn_id_idx ON public.rel_qcvn_van_ban_cong_bo_ban_hanh USING btree (ir_attachment_id, qcvn_id);

CREATE TABLE public.rel_qcvn_cong_bo_ban_hanh (
	qcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT rel_qcvn_cong_bo_ban_hanh_pkey PRIMARY KEY (qcvn_id, ir_attachment_id),
	CONSTRAINT rel_qcvn_cong_bo_ban_hanh_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT rel_qcvn_cong_bo_ban_hanh_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_qcvn_cong_bo_ban_hanh_ir_attachment_id_qcvn_id_idx ON public.rel_qcvn_cong_bo_ban_hanh USING btree (ir_attachment_id, qcvn_id);

CREATE TABLE public.ir_attachment_qcvn_rel (
	qcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT ir_attachment_qcvn_rel_pkey PRIMARY KEY (qcvn_id, ir_attachment_id),
	CONSTRAINT ir_attachment_qcvn_rel_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT ir_attachment_qcvn_rel_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX ir_attachment_qcvn_rel_ir_attachment_id_qcvn_id_idx ON public.ir_attachment_qcvn_rel USING btree (ir_attachment_id, qcvn_id);

CREATE TABLE public.rel_quy_chuan_phan_cap (
	quy_chuan_id int4 NOT NULL,
	phan_cap_id int4 NOT NULL,
	CONSTRAINT rel_quy_chuan_phan_cap_pkey PRIMARY KEY (quy_chuan_id, phan_cap_id),
	CONSTRAINT rel_quy_chuan_phan_cap_phan_cap_id_fkey FOREIGN KEY (phan_cap_id) REFERENCES public.phan_cap(id) ON DELETE CASCADE,
	CONSTRAINT rel_quy_chuan_phan_cap_quy_chuan_id_fkey FOREIGN KEY (quy_chuan_id) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_quy_chuan_phan_cap_phan_cap_id_quy_chuan_id_idx ON public.rel_quy_chuan_phan_cap USING btree (phan_cap_id, quy_chuan_id);

CREATE TABLE public.rel_phong_thu_nhiem_qcnv (
	phong_thu_nghiem_id int4 NOT NULL,
	qcvn_id int4 NOT NULL,
	CONSTRAINT rel_phong_thu_nhiem_qcnv_pkey PRIMARY KEY (phong_thu_nghiem_id, qcvn_id),
	CONSTRAINT rel_phong_thu_nhiem_qcnv_phong_thu_nghiem_id_fkey FOREIGN KEY (phong_thu_nghiem_id) REFERENCES public.phong_thu_nghiem(id) ON DELETE CASCADE,
	CONSTRAINT rel_phong_thu_nhiem_qcnv_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_phong_thu_nhiem_qcnv_qcvn_id_phong_thu_nghiem_id_idx ON public.rel_phong_thu_nhiem_qcnv USING btree (qcvn_id, phong_thu_nghiem_id);

CREATE TABLE public.rel_qcvn_ke_hoach_xay_dung (
	qcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT rel_qcvn_ke_hoach_xay_dung_pkey PRIMARY KEY (qcvn_id, ir_attachment_id),
	CONSTRAINT rel_qcvn_ke_hoach_xay_dung_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT rel_qcvn_ke_hoach_xay_dung_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_qcvn_ke_hoach_xay_dung_ir_attachment_id_qcvn_id_idx ON public.rel_qcvn_ke_hoach_xay_dung USING btree (ir_attachment_id, qcvn_id);

CREATE TABLE public.rel_qcvn_gui_tham_dinh (
	qcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT rel_qcvn_gui_tham_dinh_pkey PRIMARY KEY (qcvn_id, ir_attachment_id),
	CONSTRAINT rel_qcvn_gui_tham_dinh_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT rel_qcvn_gui_tham_dinh_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_qcvn_gui_tham_dinh_ir_attachment_id_qcvn_id_idx ON public.rel_qcvn_gui_tham_dinh USING btree (ir_attachment_id, qcvn_id);S

CREATE TABLE public.linh_vuc_qcvn_rel (
	qcvn_id int4 NOT NULL,
	linh_vuc_id int4 NOT NULL,
	CONSTRAINT linh_vuc_qcvn_rel_pkey PRIMARY KEY (qcvn_id, linh_vuc_id),
	CONSTRAINT linh_vuc_qcvn_rel_linh_vuc_id_fkey FOREIGN KEY (linh_vuc_id) REFERENCES public.linh_vuc(id) ON DELETE CASCADE,
	CONSTRAINT linh_vuc_qcvn_rel_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX linh_vuc_qcvn_rel_linh_vuc_id_qcvn_id_idx ON public.linh_vuc_qcvn_rel USING btree (linh_vuc_id, qcvn_id);

CREATE TABLE public.qcvn_wizard_search_tieu_chuan_rel (
	wizard_search_tieu_chuan_id int4 NOT NULL,
	qcvn_id int4 NOT NULL,
	CONSTRAINT qcvn_wizard_search_tieu_chuan_rel_pkey PRIMARY KEY (wizard_search_tieu_chuan_id, qcvn_id),
	CONSTRAINT qcvn_wizard_search_tieu_chuan__wizard_search_tieu_chuan_id_fkey FOREIGN KEY (wizard_search_tieu_chuan_id) REFERENCES public.wizard_search_tieu_chuan(id) ON DELETE CASCADE,
	CONSTRAINT qcvn_wizard_search_tieu_chuan_rel_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX qcvn_wizard_search_tieu_chuan_qcvn_id_wizard_search_tieu_ch_idx ON public.qcvn_wizard_search_tieu_chuan_rel USING btree (qcvn_id, wizard_search_tieu_chuan_id);

CREATE TABLE public.rel_qcvn_tham_tra (
	qcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT rel_qcvn_tham_tra_pkey PRIMARY KEY (qcvn_id, ir_attachment_id),
	CONSTRAINT rel_qcvn_tham_tra_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT rel_qcvn_tham_tra_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_qcvn_tham_tra_ir_attachment_id_qcvn_id_idx ON public.rel_qcvn_tham_tra USING btree (ir_attachment_id, qcvn_id);

CREATE TABLE public.rel_qcvn_chuyen_vien (
	qcvn_id int4 NOT NULL,
	chuyen_gia_id int4 NOT NULL,
	CONSTRAINT rel_qcvn_chuyen_vien_pkey PRIMARY KEY (qcvn_id, chuyen_gia_id),
	CONSTRAINT rel_qcvn_chuyen_vien_chuyen_gia_id_fkey FOREIGN KEY (chuyen_gia_id) REFERENCES public.chuyen_gia(id) ON DELETE CASCADE,
	CONSTRAINT rel_qcvn_chuyen_vien_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_qcvn_chuyen_vien_chuyen_gia_id_qcvn_id_idx ON public.rel_qcvn_chuyen_vien USING btree (chuyen_gia_id, qcvn_id);

CREATE TABLE public.rel_qcvn_lanh_dao (
	qcvn_id int4 NOT NULL,
	chuyen_gia_id int4 NOT NULL,
	CONSTRAINT rel_qcvn_lanh_dao_pkey PRIMARY KEY (qcvn_id, chuyen_gia_id),
	CONSTRAINT rel_qcvn_lanh_dao_chuyen_gia_id_fkey FOREIGN KEY (chuyen_gia_id) REFERENCES public.chuyen_gia(id) ON DELETE CASCADE,
	CONSTRAINT rel_qcvn_lanh_dao_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_qcvn_lanh_dao_chuyen_gia_id_qcvn_id_idx ON public.rel_qcvn_lanh_dao USING btree (chuyen_gia_id, qcvn_id);

CREATE TABLE public.rel_qcvn_xin_y_kien (
	qcvn_id int4 NOT NULL,
	ir_attachment_id int4 NOT NULL,
	CONSTRAINT rel_qcvn_xin_y_kien_pkey PRIMARY KEY (qcvn_id, ir_attachment_id),
	CONSTRAINT rel_qcvn_xin_y_kien_ir_attachment_id_fkey FOREIGN KEY (ir_attachment_id) REFERENCES public.ir_attachment(id) ON DELETE CASCADE,
	CONSTRAINT rel_qcvn_xin_y_kien_qcvn_id_fkey FOREIGN KEY (qcvn_id) REFERENCES public.qcvn(id) ON DELETE CASCADE
);
CREATE INDEX rel_qcvn_xin_y_kien_ir_attachment_id_qcvn_id_idx ON public.rel_qcvn_xin_y_kien USING btree (ir_attachment_id, qcvn_id);"""


# Chain to query
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

# _inputs = RunnableParallel(
#     {
#         "question": lambda x: x["question"],
#         "schema": get_schema,
#     }
# )

# final_rag_chain = _inputs | prompt | llm | StrOutputParser()


sql_response = prompt | llm.bind(stop=["\nSQLResult:"]) | StrOutputParser()


def get_sql(question: str):
    print(question)
    schema_description = get_schema()
    res = sql_response.invoke({"question": question, "schema": schema_description})
    print("=========================")
    print(res)
    print("=========================")
    return res
