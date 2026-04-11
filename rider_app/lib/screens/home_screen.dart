import 'dart:async';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:animate_do/animate_do.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import '../config.dart';
import '../models/order_model.dart';
import '../models/user_model.dart';
import '../providers/auth_provider.dart';
import '../services/api_service.dart';
import 'delivery_detail_screen.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  Map<String, List<OrderModel>> _deliveries = {'available': [], 'active': [], 'completed': []};
  Map<String, dynamic>? _summary;
  bool _isLoading = true;
  Timer? _refreshTimer;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _loadData();
    // Auto refresh every 30 seconds
    _refreshTimer = Timer.periodic(Duration(seconds: 30), (timer) => _loadData(showLoading: false));
  }

  @override
  void dispose() {
    _tabController.dispose();
    _refreshTimer?.cancel();
    super.dispose();
  }

  Future<void> _loadData({bool showLoading = true}) async {
    if (showLoading) setState(() => _isLoading = true);
    final user = Provider.of<AuthProvider>(context, listen: false).user;
    if (user == null) return;

    try {
      final deliveries = await ApiService.fetchDeliveries(user.id);
      final summary = await ApiService.fetchSummary(user.id);
      setState(() {
        _deliveries = deliveries;
        _summary = summary;
        _isLoading = false;
      });
    } catch (e) {
      print('Error loading data: $e');
      if (showLoading) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final user = Provider.of<AuthProvider>(context).user!;

    return Scaffold(
      appBar: AppBar(
        title: Text('Rider Dashboard', style: GoogleFonts.outfit(fontWeight: FontWeight.bold)),
        backgroundColor: AppConfig.backgroundColor,
        elevation: 0,
        actions: [
          IconButton(
            icon: Icon(Icons.logout, color: AppConfig.primaryColor),
            onPressed: () => Provider.of<AuthProvider>(context, listen: false).logout(),
          ),
        ],
      ),
      body: Column(
        children: [
          _buildSummaryCard(),
          TabBar(
            controller: _tabController,
            labelColor: AppConfig.primaryColor,
            unselectedLabelColor: AppConfig.secondaryColor,
            indicatorColor: AppConfig.accentColor,
            indicatorWeight: 3,
            labelStyle: GoogleFonts.outfit(fontWeight: FontWeight.bold),
            tabs: [
              Tab(text: 'Available'),
              Tab(text: 'Active'),
              Tab(text: 'History'),
            ],
          ),
          Expanded(
            child: _isLoading 
              ? Center(child: SpinKitFadingCircle(color: AppConfig.primaryColor))
              : TabBarView(
                  controller: _tabController,
                  children: [
                    _buildOrderList(_deliveries['available']!, 'No available orders.'),
                    _buildOrderList(_deliveries['active']!, 'No active deliveries.'),
                    _buildOrderList(_deliveries['completed']!, 'No delivery history.'),
                  ],
                ),
          ),
        ],
      ),
    );
  }

  Widget _buildSummaryCard() {
    if (_summary == null) return SizedBox();

    return FadeInDown(
      child: Container(
        margin: EdgeInsets.all(20),
        padding: EdgeInsets.all(25),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [AppConfig.primaryColor, AppConfig.secondaryColor],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(20),
          boxShadow: [
            BoxShadow(
              color: AppConfig.primaryColor.withOpacity(0.3),
              blurRadius: 15,
              offset: Offset(0, 8),
            ),
          ],
        ),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildSummaryItem('Today\'s Earnings', '₱${_summary!['today_earnings']}', FontAwesomeIcons.wallet),
                _buildSummaryItem('Completed', '${_summary!['today_deliveries']}', FontAwesomeIcons.checkDouble),
              ],
            ),
            Divider(color: Colors.white24, height: 30),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildSummaryItem('Total Walet', '₱${_summary!['wallet_balance']}', FontAwesomeIcons.coins),
                _buildSummaryItem('Active Now', '${_summary!['active_deliveries']}', FontAwesomeIcons.personRunning),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSummaryItem(String label, String value, IconData icon) {
    return Row(
      children: [
        Container(
          padding: EdgeInsets.all(10),
          decoration: BoxDecoration(color: Colors.white12, borderRadius: BorderRadius.circular(12)),
          child: Icon(icon, color: Colors.white, size: 20),
        ),
        SizedBox(width: 15),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: GoogleFonts.inter(color: Colors.white70, fontSize: 12)),
            Text(value, style: GoogleFonts.outfit(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
      ],
    );
  }

  Widget _buildOrderList(List<OrderModel> orders, String emptyMsg) {
    if (orders.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.inbox_outlined, size: 80, color: Colors.grey[400]),
            SizedBox(height: 10),
            Text(emptyMsg, style: GoogleFonts.inter(color: Colors.grey)),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: () => _loadData(showLoading: false),
      child: ListView.builder(
        padding: EdgeInsets.all(15),
        itemCount: orders.length,
        itemBuilder: (context, index) {
          final order = orders[index];
          return FadeInUp(
            delay: Duration(milliseconds: 100 * index),
            child: _buildOrderCard(order),
          );
        },
      ),
    );
  }

  Widget _buildOrderCard(OrderModel order) {
    return Card(
      elevation: 0,
      margin: EdgeInsets.only(bottom: 15),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15), side: BorderSide(color: Colors.grey[200]!)),
      child: InkWell(
        onTap: () => _showOrderDetails(order),
        borderRadius: BorderRadius.circular(15),
        child: Padding(
          padding: EdgeInsets.all(15),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('Order #${order.id}', style: GoogleFonts.outfit(fontWeight: FontWeight.bold, fontSize: 16)),
                  _buildStatusBadge(order),
                ],
              ),
              Divider(height: 25),
              Row(
                children: [
                  Icon(Icons.location_on, size: 18, color: AppConfig.accentColor),
                  SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      order.deliveryAddress,
                      style: GoogleFonts.inter(fontSize: 14),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ],
              ),
              SizedBox(height: 10),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('${order.items.length} items • ₱${order.totalAmount}', style: GoogleFonts.inter(color: AppConfig.secondaryColor, fontWeight: FontWeight.bold)),
                  Text(order.paymentMethod, style: GoogleFonts.inter(fontSize: 12, color: Colors.grey)),
                ],
              ),
              if (order.deliveryStatus == 'WAITING' || order.deliveryStatus == null)
                Padding(
                  padding: const EdgeInsets.only(top: 15),
                  child: SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () => _acceptOrder(order),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppConfig.primaryColor,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                      child: Text('ACCEPT DELIVERY', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatusBadge(OrderModel order) {
    Color color;
    String text = order.deliveryStatus ?? 'WAITING';

    switch (text) {
      case 'DELIVERED': color = Colors.green; break;
      case 'ON_THE_WAY': color = Colors.orange; break;
      case 'PICKED_UP': color = Colors.blue; break;
      default: color = AppConfig.accentColor;
    }

    return Container(
      padding: EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
      child: Text(text, style: TextStyle(color: color, fontSize: 10, fontWeight: FontWeight.bold)),
    );
  }

  void _showOrderDetails(OrderModel order) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => DeliveryDetailScreen(
          order: order,
          onUpdate: () => _loadData(showLoading: false),
        ),
      ),
    );
  }

  Future<void> _acceptOrder(OrderModel order) async {
    final user = Provider.of<AuthProvider>(context, listen: false).user!;
    final success = await ApiService.acceptOrder(order.id, user.id);
    if (success) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Order Accepted!')));
      _loadData(showLoading: false);
      _tabController.animateTo(1); // Switch to Active tab
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Could not accept order.')));
    }
  }
}
