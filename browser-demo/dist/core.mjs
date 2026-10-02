export function scoreRows(rows,m){
 if(!Array.isArray(rows)||!rows.length||rows.length>20000)throw Error('Provide between 1 and 20,000 customers.');
 const ids=new Set();return rows.map((r,i)=>{
  const id=String(r.customer_id??'').trim();if(!id||ids.has(id))throw Error(`Row ${i+1}: customer IDs must be present and unique.`);ids.add(id);
  const raw=m.numeric.filter(k=>k!=='usage_change').concat(m.categorical);
  for(const key of raw)if(!(key in r))throw Error(`Missing column: ${key}`);
  const nums=m.numeric.slice(0,-1).map(k=>{const x=r[k];if(x==null||String(x).trim()==='')return null;const v=Number(x);if(!Number.isFinite(v)||v<0)throw Error(`Row ${i+1}: ${k} must be a nonnegative number or blank.`);return v;});
  const cats=m.categorical.map((k,j)=>{let c=String(r[k]??'').trim().toLowerCase();if(!c)return m.modes[j];if(!m.categories[j].includes(c))throw Error(`Row ${i+1}: invalid ${k}. Use ${m.categories[j].join(' or ')}.`);return c;});
  const change=nums[2]===null||nums[3]===null||nums[2]===0?null:(nums[3]-nums[2])/nums[2];nums.push(change);
  const values=nums.map((x,j)=>((x??m.medians[j])-m.means[j])/m.scales[j]);
  cats.forEach((c,j)=>m.categories[j].forEach(v=>values.push(c===v?1:0)));
  const z=values.reduce((s,v,j)=>s+v*m.coefficients[j],m.intercept);const probability=z>=0?1/(1+Math.exp(-z)):Math.exp(z)/(1+Math.exp(z));
  const contact=probability>=m.threshold;let action='Regular engagement';
  if(contact)action=(nums[5]??0)>0?'Billing assistance':(nums[4]??0)>=3?'Resolve support issues':(change??0)<-.25?'Offer onboarding session':'Review needs with customer';
  return {customer_id:id,contract:cats[0],monthly_charge:nums[1],churn_probability:probability,contact_recommended:contact,risk_band:probability<=.3?'Low':probability<=.6?'Medium':'High',suggested_action:action,source_index:i};
 }).sort((a,b)=>b.churn_probability-a.churn_probability||a.source_index-b.source_index).map((r,i)=>({...r,priority_rank:i+1}));
}
export function parseCSV(text){
 text=text.replace(/^\uFEFF/,'');let rows=[],row=[],v='',quoted=false;
 for(let i=0;i<text.length;i++){const c=text[i];if(c==='"'){if(quoted&&text[i+1]==='"'){v+='"';i++;}else quoted=!quoted;}
 else if(c===','&&!quoted){row.push(v);v='';}else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&text[i+1]==='\n')i++;row.push(v);if(row.some(x=>x.trim()))rows.push(row);row=[];v='';}else v+=c;}
 if(quoted)throw Error('CSV contains an unclosed quoted field.');row.push(v);if(row.some(x=>x.trim()))rows.push(row);
 if(rows.length<2)throw Error('CSV must contain a header and customer rows.');const headers=rows.shift().map(x=>x.trim());
 if(new Set(headers).size!==headers.length||headers.some(x=>!x))throw Error('Column names must be unique and nonblank.');
 return rows.map((r,i)=>{if(r.length!==headers.length)throw Error(`Row ${i+2}: unexpected number of columns.`);return Object.fromEntries(headers.map((k,j)=>[k,r[j]]));});
}
export function toCSV(rows){
 if(!rows.length)return '';const keys=Object.keys(rows[0]).filter(x=>x!=='source_index');const cell=x=>{let s=x==null?'':String(x);if(typeof x==='string'&&/^[=+@\-\t\r]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';};return [keys,...rows.map(r=>keys.map(k=>r[k]))].map(row=>row.map(cell).join(',')).join('\r\n');
}
