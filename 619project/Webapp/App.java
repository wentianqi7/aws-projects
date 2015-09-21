package com.mastertheboss.undertow;

import java.util.NavigableMap;
import java.util.Collection;
import java.util.TreeMap;

import java.io.BufferedReader;
import java.io.FileReader;

import java.nio.ByteBuffer;
import java.nio.charset.Charset;
import java.util.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.math.BigInteger;
import io.undertow.io.Sender;
import java.lang.Long;
import java.util.concurrent.ConcurrentMap;
import io.undertow.Undertow;
import io.undertow.UndertowOptions;
import io.undertow.io.IoCallback;
import io.undertow.server.HttpHandler;
import io.undertow.server.HttpServerExchange;
import io.undertow.util.Headers;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.hbase.client.HTablePool;
import org.apache.hadoop.hbase.client.HTableInterface;
import org.apache.hadoop.hbase.KeyValue;
import com.googlecode.concurrentlinkedhashmap.ConcurrentLinkedHashMap;

public class App {
	private final static int NUM_CONNECTIONS = 100;
	private static HTablePool pool;
	private static HTableInterface q2;
	private static HTableInterface q3;
	private static HTableInterface q4;
	private static HTableInterface q5;
	//private static HTableInterface q6;
	private final byte[] T = Bytes.toBytes("content");
	private final byte[] EMPTY = Bytes.toBytes("");
	private ConcurrentMap<String, String> cache3;
	private final NavigableMap<Long, Integer> map6 = new TreeMap<Long, Integer>();

	public App() throws Exception {
		cache3 = new ConcurrentLinkedHashMap.Builder<String, String>()
				.maximumWeightedCapacity(3000000)
				.build();
		BufferedReader in = new BufferedReader(new FileReader("q6_map"));
		String line = "";
		while ((line = in.readLine()) != null) {
	        	String parts[] = line.trim().split("\t");
			if(parts.length<2) continue;
       			map6.put(Long.parseLong(parts[0]), Integer.parseInt(parts[1]));
        	}
	        in.close();
		System.out.print("NavigableMap initialization complete");
		pool = new HTablePool(HBaseConfiguration.create(), NUM_CONNECTIONS);
		q2 = pool.getTable(Bytes.toBytes("tw_q2"));
		q3 = pool.getTable(Bytes.toBytes("tw_q3"));
		q4 = pool.getTable(Bytes.toBytes("q4_test"));
		q5 = pool.getTable(Bytes.toBytes("q5_test"));
		//q6 = pool.getTable(Bytes.toBytes("q6"));
	}

	public String getQ2(String key) throws Exception {
		//Get g = new Get(Bytes.toBytes(key));
		//return Bytes.toString(q2.get(g).getValue(T, EMPTY)); 
		Get get = new Get(key.getBytes());
            	Result rs = q2.get(get);
		KeyValue kv =(KeyValue)rs.list().get(0);
		String result = new String(kv.getValue(),"UTF-8");
		result += "\n";
		return result;
	}

	public String getQ3(String userid) throws Exception {
		if (cache3.containsKey(userid)) {
			return cache3.get(userid);
		}
		Get g = new Get(Bytes.toBytes(userid));
		Result r =  q3.get(g);
		String result = Bytes.toString(r.getValue(T, EMPTY));
		cache3.put(userid, result);
		return result;
	}

	public String getQ4(String date, String location,int minrank, int maxrank) throws Exception {
		String key = location+"*"+date;
		Get g = new Get(key.getBytes());
                Result rs = q4.get(g);
		KeyValue kv = (KeyValue)rs.list().get(0);
                String temp = new String(kv.getValue(),"UTF-8");
		String[] words = temp.split("\\*");
		int len = words.length;
		if(len<maxrank) maxrank = len;
		StringBuffer sb = new StringBuffer();
		for(int i=minrank;i<maxrank;i++){
			sb.append(words[i]);
		}
		return sb.toString();
		
/*
		int min_len = minrank.length(), max_len= maxrank.length();
		switch(min_len){
			case 1:
				minrank = "0000"+minrank;
				break;
			case 2:
				minrank = "000"+minrank;
				break;
			case 3:
				minrank = "00"+minrank;
				break;
			case 4:
				minrank = "0"+minrank;
				break;
		}
		
		switch(max_len){
			case 1:
				maxrank = "0000"+maxrank;
                                break;
                        case 2:
				maxrank = "000"+maxrank;
                                break;
                        case 3:
				maxrank = "00"+maxrank;
                                break;
                        case 4:
				maxrank = "0"+maxrank;
                                break;
		}
		StringBuffer key = new StringBuffer();
		key.append(location);
		key.append("*");
		key.append(date);
		key.append("*");
		String minkey = key.toString()+minrank;
		String maxkey = key.toString()+maxrank;
		Scan scan = new Scan();
		scan.setStartRow(Bytes.toBytes(minkey));
		scan.setStopRow(Bytes.toBytes(maxkey));
		ResultScanner r = q4.getScanner(scan);
		Result res = null;
		StringBuffer result = new StringBuffer();
		while ((res = r.next()) != null) {
			result.append(Bytes.toString(res.getValue(T, EMPTY)));
		}
		return result.toString();
*/
	}

	public String getQ5(String uid1, String uid2) throws Exception {
		Get get = new Get(uid1.getBytes());
                Result rs = q5.get(get);
                StringBuffer result = new StringBuffer();
		String temp1 = new String(rs.getValue(T,EMPTY));
		String[] scores1 = temp1.trim().split(":");

		get = new Get(uid2.getBytes());
		rs = q5.get(get);
		String temp2 = new String(rs.getValue(T,EMPTY));
		String[] scores2 = temp2.trim().split(":");

		result.append(uid1);
		result.append("\t");
		result.append(uid2);
		result.append("\tWINNER\n");

		for(int i=1;i<5;i++){
			long score1 = Long.parseLong(scores1[i%4]);
			long score2 = Long.parseLong(scores2[i%4]);
			result.append(score1);
			result.append("\t");
			result.append(score2);
			result.append("\t");
			if(score1>score2) result.append(uid1);
			else if(score1<score2) result.append(uid2);
			else result.append("X");
			result.append("\n");
		}
                
                return result.toString();
	}

	public String getQ6(long min, long max) throws Exception {		
		int low = map6.lowerEntry(min).getValue();
		int high = map6.floorEntry(max).getValue();
		return Integer.toString(high-low)+"\n";	
	}

	public static void main(String[] args) throws Exception {
		final String info = "BiliBili,512512512512,612412512412,8241241\n";
		final SimpleDateFormat fmt = new SimpleDateFormat("YYYY-MM-dd HH:mm:ss");
		final BigInteger publicKey = new BigInteger("6876766832351765396496377534476050002970857483815262918450355869850085167053394672634315391224052153");
		final Charset utf8 = Charset.forName("UTF-8");
		final App home = new App();
		
		Undertow.builder()
		.setWorkerThreads(4096)
		.setIoThreads(Runtime.getRuntime().availableProcessors() * 2)
		.setServerOption(UndertowOptions.ALWAYS_SET_KEEP_ALIVE, false)
		.setBufferSize(1024*16)
		.addHttpListener(80, "0.0.0.0")
		.setHandler(new HttpHandler() {

			public void handleRequest(final HttpServerExchange exchange) throws Exception {
				char path = exchange.getRequestPath().charAt(2);
				String result = null;
				Map<String,Deque<String>> queryMap = null;
				exchange.getResponseHeaders().put(Headers.CONTENT_TYPE, "text/plain; charset=utf-8");

				switch (path) {
				case '1':
					queryMap = exchange.getQueryParameters();
			                String s = queryMap.get("key").getFirst();
                	    	        BigInteger input = new BigInteger(s);
		                        Sender sender = exchange.getResponseSender();
                		        StringBuilder sb = new StringBuilder();
		                        sb.append(input.divide(publicKey));
        		                sb.append("\n");
		                        sb.append(info);
        		                sb.append(fmt.format(Calendar.getInstance().getTime()));
	                	        sender.send(sb.toString());
					break;
				case '2':
					queryMap = exchange.getQueryParameters();
					exchange.getResponseSender().send(ByteBuffer.wrap(
							info.concat(home.getQ2(queryMap.get("userid").getFirst() + "+" 
									+ queryMap.get("tweet_time").getFirst())
									).getBytes(utf8)
							), IoCallback.END_EXCHANGE);
					break;

				case '3':
					queryMap = exchange.getQueryParameters();
					result = home.getQ3(queryMap.get("userid").getFirst());
					exchange.getResponseSender().send(ByteBuffer.wrap(
							info.concat(result).getBytes(utf8)
							), IoCallback.END_EXCHANGE);
					break;

				case '4':
					queryMap = exchange.getQueryParameters();
					String date = queryMap.get("date").getFirst();
					String location = queryMap.get("location").getFirst();
					int minrank = Integer.parseInt(queryMap.get("m").getFirst())-1;
					int maxrank = Integer.parseInt(queryMap.get("n").getFirst());
					result = home.getQ4(date,location,minrank,maxrank);
					exchange.getResponseSender().send(ByteBuffer.wrap(
							info.concat(result).getBytes(utf8)
							), IoCallback.END_EXCHANGE);
					break;

				case '5':
					queryMap = exchange.getQueryParameters();
					String uid1 = queryMap.get("m").getFirst();
					String uid2 = queryMap.get("n").getFirst();
					result = home.getQ5(uid1, uid2);
					exchange.getResponseSender().send(ByteBuffer.wrap(
                                                        info.concat(result).getBytes(utf8)
                                                        ), IoCallback.END_EXCHANGE);
					break;

				case '6':
					queryMap = exchange.getQueryParameters();
					long min = Long.parseLong(queryMap.get("m").getFirst());
                                        long max = Long.parseLong(queryMap.get("n").getFirst());
                                        result = home.getQ6(min, max);
					exchange.getResponseSender().send(ByteBuffer.wrap(
							info.concat(result).getBytes(utf8)
							), IoCallback.END_EXCHANGE);
					break;

				}
			}
		}).build().start();
	}
}
