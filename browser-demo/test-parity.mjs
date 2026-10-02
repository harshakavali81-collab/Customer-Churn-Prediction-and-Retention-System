import fs from 'node:fs';import assert from 'node:assert/strict';import {scoreRows,parseCSV,toCSV} from './dist/core.mjs';
const model=JSON.parse(fs.readFileSync('dist/model.json')),tests=JSON.parse(fs.readFileSync('dist/parity.json'));
const scores=scoreRows(tests.rows,model);let max=0;for(const row of scores){max=Math.max(max,Math.abs(row.churn_probability-tests.expected[row.source_index]));}assert(max<1e-9);
assert.throws(()=>scoreRows([tests.rows[0],tests.rows[0]],model));assert.throws(()=>scoreRows([{...tests.rows[0],usage_current:-1}],model));assert.throws(()=>scoreRows([{...tests.rows[0],contract:'bad'}],model));assert.throws(()=>scoreRows([],model));
assert.equal(parseCSV('a,b\r\n"one,two","he said ""yes"""')[0].b,'he said "yes"');assert.throws(()=>parseCSV('a,b\n"unclosed'));
assert(toCSV([{customer_id:'=1+1'}]).includes("'=1+1"));
console.log(JSON.stringify({checked:tests.rows.length,max_probability_difference:max,input_validation:'passed',csv_parser:'passed'}));
