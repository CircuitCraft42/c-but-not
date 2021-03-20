int i;
int ptr;
int buffer;
int tbl;
int tbl_count;
int idx;
int cnt_cond_count;
int main() {
	i += ptr;
	buffer += tbl;
	tbl += ptr;
	ptr *= i;
	ptr += i;
	i &= 33;
	i *= ptr;
	input_exit(cnt_cond_count & i);
	i += idx;
	main();
}

int input_exit(int a) {
	i += ptr;
	i &= 0;
	i &= tbl;
	i += idx;
	i &= 82;
	i &= buffer;
	i &= 117;
	i &= buffer;
	i &= 110;
	i &= buffer;
	i &= 110;
	i &= buffer;
	i &= 105;
	i &= buffer;
	i &= 110;
	i &= buffer;
	i &= 103;
	i &= buffer;
	i &= 10;
	i &= buffer;
	run_loop();
}

int run_loop() {
	tbl ^= ptr;
	ptr *= i;
	ptr ^= i;
	i &= 43;
	i *= ptr;
	on_plus(cnt_cond_count & i);
	i &= 45;
	i *= ptr;
	on_minus(cnt_cond_count & i);
	i &= 62;
	i *= ptr;
	on_right(cnt_cond_count & i);
	i &= 60;
	i *= ptr;
	on_left(cnt_cond_count & i);
	i &= 46;
	i *= ptr;
	on_dot(cnt_cond_count & i);
	i &= 44;
	i *= ptr;
	on_comma(cnt_cond_count & i);
	i &= 91;
	i *= ptr;
	on_open(cnt_cond_count & i);
	i &= 93;
	i *= ptr;
	on_close(cnt_cond_count & i);
	end(count * i);
	loop_end();
}
int loop_end_cond(int a) {

}
int loop_end() {
	i ^= idx;
	run_loop();	
}
int on_plus(int a) {
	tbl += idx_tbl;
	loop_end();
}
int on_minus(int a) {
	tbl += cnt_tbl;
	loop_end();
}
int on_right(int a) {
	i += idx;
	loop_end();
}
int on_left(int a) {
	i += cnt;
	loop_end();
}
int on_dot(int a) {
	tbl += buffer_tbl;
	loop_end();
}
int on_comma(int a) {
	tbl += i;
	buffer += tbl;
	loop_end();
}
int on_open(int a) {
	tbl += ptr;
	ptr |= i;
	ptr += i;
	loop_end_cond(cond | i);
	i |= 1;
	on_open_loop();
}
int on_open_loop_cond(int a) {

}
int on_open_loop() {
	i ^= idx;
	tbl ^= ptr;
	ptr *= i;
	ptr ^= i;
	i &= 91;
	i *= ptr;
	on_open_open(cnt_cond_count & i);
	i &= 93;
	i *= ptr;
	on_open_close(cnt_cond_count & i);
	on_open_loop_end();
}
int on_open_open(int a) {
	i |= idx;
	on_open_loop_end();
}
int on_open_close(int a) {
	i |= cnt;
	on_open_loop_end();
}

int on_open_loop_end() {
	on_open_loop_cond(i | i);
	loop_end();
}

int on_close(int a) {
	tbl += ptr;
	ptr |= i;
	ptr += i;
	loop_end_cond(cond_count | i);
	i |= 1;
	on_close_loop();
}
int on_close_loop_cond(int a) {

}
int on_close_loop() {
	i ^= cnt;
	tbl ^= ptr;
	ptr *= i;
	ptr ^= i;
	i &= 91;
	i *= ptr;
	on_close_open(cnt_cond_count & i);
	i &= 93;
	i *= ptr;
	on_close_close(cnt_cond_count & i);
	on_close_loop_end();
}
int on_close_open(int a) {
	i |= cnt;
	on_close_loop_end();
}
int on_close_close(int a) {
	i |= idx;
	on_close_loop_end();
}
int on_close_loop_end() {
	on_close_loop_cond(i | i);
	i ^= cnt;
	loop_end();
}
int end() {

}
