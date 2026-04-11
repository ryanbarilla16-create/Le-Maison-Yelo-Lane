import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:animate_do/animate_do.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import '../config.dart';
import '../models/order_model.dart';
import '../services/api_service.dart';
import '../providers/auth_provider.dart';
import 'package:provider/provider.dart';

class DeliveryDetailScreen extends StatefulWidget {
  final OrderModel order;
  final Function onUpdate;

  DeliveryDetailScreen({required this.order, required this.onUpdate});

  @override
  _DeliveryDetailScreenState createState() => _DeliveryDetailScreenState();
}

class _DeliveryDetailScreenState extends State<DeliveryDetailScreen> {
  bool _isLoading = false;

  Future<void> _updateStatus(String newStatus) async {
    setState(() => _isLoading = true);
    final user = Provider.of<AuthProvider>(context, listen: false).user!;
    
    try {
      final success = await ApiService.updateStatus(widget.order.id, user.id, newStatus);
      if (success) {
        widget.onUpdate();
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Status updated to $newStatus')));
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed to update status.')));
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    } finally {
      setState(() => _isLoading = false);
    }
  }

  void _callCustomer() async {
    if (widget.order.customerPhone == null) return;
    final Uri url = Uri.parse('tel:${widget.order.customerPhone}');
    if (await canLaunchUrl(url)) {
      await launchUrl(url);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text('Order Details', style: GoogleFonts.outfit(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildOrderHeader(),
            SizedBox(height: 30),
            _buildCustomerSection(),
            SizedBox(height: 30),
            _buildItemsSection(),
            SizedBox(height: 100), // Space for action button
          ],
        ),
      ),
      bottomSheet: _buildActionButton(),
    );
  }

  Widget _buildOrderHeader() {
    return FadeInDown(
      child: Container(
        padding: EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: AppConfig.backgroundColor,
          borderRadius: BorderRadius.circular(20),
        ),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Order ID', style: TextStyle(color: AppConfig.secondaryColor, fontSize: 12)),
                    Text('#${widget.order.id}', style: GoogleFonts.outfit(fontSize: 24, fontWeight: FontWeight.bold)),
                  ],
                ),
                Container(
                  padding: EdgeInsets.symmetric(horizontal: 15, vertical: 8),
                  decoration: BoxDecoration(color: AppConfig.primaryColor, borderRadius: BorderRadius.circular(10)),
                  child: Text('₱${widget.order.totalAmount}', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                ),
              ],
            ),
            Divider(height: 40),
            _buildDetailRow(Icons.payment, 'Payment Method', widget.order.paymentMethod, widget.order.paymentStatus),
            SizedBox(height: 15),
            _buildDetailRow(Icons.delivery_dining, 'Delivery Status', widget.order.deliveryStatus, widget.order.deliveryStatus),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailRow(IconData icon, String label, String value, String status) {
    return Row(
      children: [
        Icon(icon, size: 20, color: AppConfig.secondaryColor),
        SizedBox(width: 15),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: TextStyle(color: Colors.grey, fontSize: 12)),
            Text(value, style: TextStyle(fontWeight: FontWeight.bold)),
          ],
        ),
        Spacer(),
        if (status == 'PAID') Icon(Icons.check_circle, color: Colors.green, size: 16),
      ],
    );
  }

  Widget _buildCustomerSection() {
    return FadeInLeft(
      delay: Duration(milliseconds: 200),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('CUSTOMER & DELIVERY', style: GoogleFonts.outfit(fontWeight: FontWeight.bold, letterSpacing: 1.2, color: Colors.grey)),
          SizedBox(height: 15),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: CircleAvatar(backgroundColor: AppConfig.accentColor, child: Icon(Icons.person, color: Colors.white)),
            title: Text(widget.order.customerName, style: TextStyle(fontWeight: FontWeight.bold)),
            subtitle: Text(widget.order.customerPhone ?? 'No phone provided'),
            trailing: IconButton(
              icon: Icon(Icons.phone, color: Colors.green),
              onPressed: _callCustomer,
            ),
          ),
          SizedBox(height: 10),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(Icons.location_on, color: AppConfig.primaryColor),
              SizedBox(width: 15),
              Expanded(child: Text(widget.order.deliveryAddress, style: TextStyle(fontSize: 16))),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildItemsSection() {
    return FadeInLeft(
      delay: Duration(milliseconds: 400),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('ORDER ITEMS (${widget.order.items.length})', style: GoogleFonts.outfit(fontWeight: FontWeight.bold, letterSpacing: 1.2, color: Colors.grey)),
          SizedBox(height: 15),
          ...widget.order.items.map((item) => Padding(
            padding: const EdgeInsets.only(bottom: 10),
            child: Row(
              children: [
                Container(
                  width: 30, height: 30,
                  alignment: Alignment.center,
                  decoration: BoxDecoration(color: AppConfig.backgroundColor, shape: BoxShape.circle),
                  child: Text('${item.quantity}x', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                ),
                SizedBox(width: 15),
                Expanded(child: Text(item.name)),
                Text('₱${item.price}'),
              ],
            ),
          )).toList(),
        ],
      ),
    );
  }

  Widget _buildActionButton() {
    String? nextStatus;
    String? btnText;
    IconData? icon;

    if (widget.order.deliveryStatus == 'WAITING' || widget.order.deliveryStatus == null) {
      if (widget.order.kitchenStatus == 'COMPLETED') {
        nextStatus = 'PICKED_UP';
        btnText = 'MARK AS PICKED UP';
        icon = Icons.shopping_bag;
      } else {
        return Container(
          padding: EdgeInsets.all(20),
          color: Colors.orange.withOpacity(0.1),
          child: Row(
            children: [
              SpinKitPulse(color: Colors.orange, size: 20),
              SizedBox(width: 15),
              Expanded(child: Text('Wait for Kitchen to complete order before picking up.', style: TextStyle(color: Colors.orange, fontWeight: FontWeight.bold))),
            ],
          ),
        );
      }
    } else if (widget.order.deliveryStatus == 'PICKED_UP') {
      nextStatus = 'ON_THE_WAY';
      btnText = 'START DELIVERY (ON THE WAY)';
      icon = Icons.directions_bike;
    } else if (widget.order.deliveryStatus == 'ON_THE_WAY') {
      nextStatus = 'DELIVERED';
      btnText = 'MARK AS DELIVERED';
      icon = Icons.check_circle;
    }

    if (nextStatus == null) return SizedBox();

    return Padding(
      padding: EdgeInsets.all(20),
      child: SizedBox(
        width: double.infinity,
        height: 60,
        child: ElevatedButton.icon(
          onPressed: _isLoading ? null : () => _updateStatus(nextStatus!),
          icon: _isLoading ? SizedBox() : Icon(icon, color: Colors.white),
          label: _isLoading 
            ? SpinKitThreeBounce(color: Colors.white, size: 20)
            : Text(btnText!, style: GoogleFonts.outfit(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.white)),
          style: ElevatedButton.styleFrom(
            backgroundColor: AppConfig.primaryColor,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
            elevation: 5,
          ),
        ),
      ),
    );
  }
}
